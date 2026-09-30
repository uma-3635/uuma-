import sqlite3
import time
from contextlib import contextmanager
from typing import Iterator

from .config import get_settings


@contextmanager
def _connection() -> Iterator[sqlite3.Connection]:
    settings = get_settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(settings.database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db() -> None:
    with _connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                expires_at INTEGER NOT NULL
            );
            """
        )


def create_user(username: str, email: str, password_hash: str) -> dict | None:
    with _connection() as connection:
        try:
            cursor = connection.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash),
            )
        except sqlite3.IntegrityError:
            return None
        row = connection.execute(
            "SELECT id, username, email FROM users WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)


def get_user_by_email(email: str) -> dict | None:
    with _connection() as connection:
        row = connection.execute(
            "SELECT id, username, email, password_hash FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    return dict(row) if row else None


def create_session(token: str, user_id: int, expires_at: int) -> None:
    with _connection() as connection:
        connection.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user_id, expires_at),
        )


def get_user_by_session(token: str) -> dict | None:
    with _connection() as connection:
        row = connection.execute(
            """
            SELECT users.id, users.username, users.email
            FROM users
            JOIN sessions ON sessions.user_id = users.id
            WHERE sessions.token = ? AND sessions.expires_at > ?
            """,
            (token, int(time.time())),
        ).fetchone()
    return dict(row) if row else None


def delete_session(token: str) -> None:
    with _connection() as connection:
        connection.execute("DELETE FROM sessions WHERE token = ?", (token,))
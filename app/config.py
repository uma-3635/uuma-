import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    app_name: str
    database_path: Path
    static_dir: Path


def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "PocketSmart AI"),
        database_path=Path(
            os.getenv("DATABASE_PATH", str(PROJECT_ROOT / "pocketsmart.db"))
        ),
        static_dir=PROJECT_ROOT / "static",
    )
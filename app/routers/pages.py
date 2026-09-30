from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home() -> str:
    return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>PocketSmart AI</title></head>
<body><main><h1>PocketSmart AI</h1><p>API is running.</p>
<p><a href="/docs">Open API documentation</a></p></main></body></html>"""
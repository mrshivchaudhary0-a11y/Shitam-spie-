"""Username Finder: checks many public sites in parallel and streams results live."""
import asyncio
import json
import re
import time
from collections import defaultdict, deque
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse

BASE = Path(__file__).parent
SITES = json.loads((BASE / "sites.json").read_text(encoding="utf-8"))
USERNAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,40}$")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
MAX_CONCURRENCY = 20  # requests in flight at once
TIMEOUT = 10          # seconds per site
RATE_LIMIT = 10       # searches per minute per IP
hits = defaultdict(deque)

app = FastAPI(title="Username Finder")


async def check_site(client, sem, site, username):
    """Return {"site", "url", "status"}; status is found / not_found / error."""
    result = {
        "site": site["name"],

"""Username & phone lookup. Username checks run in parallel and stream live."""
import asyncio
import json
import os
import re
from pathlib import Path

import httpx
import phonenumbers
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from phonenumbers import PhoneNumberType, carrier, geocoder, timezone

BASE = Path(__file__).parent
SITES = json.loads((BASE / "sites.json").read_text(encoding="utf-8"))
USERNAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,40}$")
PHONE_RE = re.compile(r"^\+?[0-9 ()\-]{5,25}$")
DEFAULT_REGION = os.environ.get("DEFAULT_REGION", "IN")  # for numbers without +country code
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
MAX_CONCURRENCY = 30  # requests in flight at once
TIMEOUT = 10          # seconds per site
LINE_TYPES = {
    PhoneNumberType.FIXED_LINE: "Landline",
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Landline or mobile",
    PhoneNumberType.TOLL_FREE: "Toll free",
    PhoneNumberType.PREMIUM_RATE: "Premium rate",
    PhoneNumberType.SHARED_COST: "Shared cost",

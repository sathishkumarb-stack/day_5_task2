import os
import secrets
from dotenv import load_dotenv
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()

API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key is missing"
        )

    if not API_KEY or not secrets.compare_digest(api_key, API_KEY):
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )

    return api_key
import os
from fastapi import Header, HTTPException

def require_api_key(x_api_key: str | None = Header(default=None)):
    expected = os.getenv("ANALYTICS_API_KEY")
    if not expected:
        raise HTTPException(status_code=500, detail="Server misconfigured: ANALYTICS_API_KEY not set")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True

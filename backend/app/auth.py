from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader
import os

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    expected_api_key = os.getenv("API_KEY", "dev-api-key-12345")
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

def require_auth(api_key: str = Depends(get_api_key)):
    return api_key

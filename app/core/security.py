from fastapi import HTTPException, status, Request
from fastapi.security import APIKeyHeader
from .config import get_settings

settings = get_settings()
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME)

async def validate_api_key(request: Request):
    api_key = request.headers.get(settings.API_KEY_NAME)
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key 
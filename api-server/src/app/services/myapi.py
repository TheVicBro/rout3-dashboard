import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.repositories import myapi_repository as myapi_repo

API_KEY_NAME = "api_key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def generate_api_key():
    return secrets.token_hex()  # Generates a 64-character hex string


def get_api_key_from_header(api_key_header: str = Security(api_key_header)):
    return api_key_header


def verify_api_key(db: Session, api_key_string):
    api_key = myapi_repo.get_myapi(db, api_key_string)
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return api_key

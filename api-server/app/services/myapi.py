import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.repositories import myapi_repo

API_KEY_NAME = "myapi_key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def generate_api_key():
    return secrets.token_hex()  # Generates a 64-character hex string


# Security used instead of Depends(), for context and openapi docs? Maybe more?
def get_api_key_from_header(api_key_header: str = Security(api_key_header)):
   return api_key_header


def verify_api_key(db: Session, api_key_string):
    api_key = myapi_repo.get_myapi(db, api_key_string)
    if api_key is None:
        return False
    return True

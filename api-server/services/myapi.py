from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from db.database import get_db
from db.repositories import user_repository as user_repo
from db.repositories import myapi_repository as myapi_repo
from services.security import verify_password
from services import jwt
from typing_extensions import Annotated
from models.models import User

import secrets

API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

key = ""


def generate_api_key():
    global key
    key = secrets.token_hex()
    return key  # Generates a 64-character hex string


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

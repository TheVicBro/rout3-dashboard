from datetime import datetime, timedelta, timezone
from typing import Any
from cryptography.fernet import Fernet, MultiFernet

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
KEY1 = Fernet(settings.FERNET_KEY1)
KEY2 = Fernet(settings.FERNET_KEY2)

multifernet = MultiFernet([KEY1, KEY2])


ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(sub: str, expires_delta: timedelta) -> Token:
    to_encode = {"sub": sub}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt_token = jwt.encode(
        to_encode, settings.JWT_SIGNING_KEY, algorithm=ALGORITHM
    )

    return Token(access_token=encoded_jwt_token, token_type="Bearer")


def encrypt_data(data: str) -> bytes:
    bytes_data = bytes(data, "utf-8")
    print(bytes_data)
    return multifernet.encrypt(bytes_data)


def decrypt_data(encrypted_data: bytes) -> str:
    rotated_data = multifernet.rotate(encrypted_data)
    return multifernet.decrypt(rotated_data).decode("utf-8")

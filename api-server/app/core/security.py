from datetime import datetime, timedelta, timezone
from typing import Any
from cryptography.fernet import Fernet, MultiFernet

import jwt
import hashlib
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


def hash_api_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def fernet_encrypt_data(data: str) -> str:
    bytes_data = bytes(data, "utf-8")
    encrypted = multifernet.encrypt(bytes_data)
    return encrypted.decode("utf-8")


def fernet_decrypt_data(encrypted_data) -> str:
    rotated_data = multifernet.rotate(encrypted_data)
    decrypted_data = multifernet.decrypt(rotated_data)
    return decrypted_data.decode("utf-8")  # Decode bytes to string

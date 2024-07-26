from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from db.database import get_db
from db.repositories import user_repository as user_repo
from services.auth.security import verify_password
from services.auth import jwt

security = HTTPBasic()


def verification(username: str, plaintext_password: str, db: Session):
    user = user_repo.get_user_by_username(db, username)
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user is None:
        raise unauthorized_exception

    verification = verify_password(
        plaintext_password=plaintext_password, hashed_password=user.hashed_password
    )

    if verification:
        return jwt.login_for_access_token(userid=user.id, username=username)
    else:
        raise unauthorized_exception


def get_current_user(creds: HTTPBasicCredentials = Depends(security)):
    return creds.username

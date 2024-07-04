from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from db.database import get_db
from db.repositories import user_repository as user_repo
from services.security import verify_password
from services import jwt
from typing_extensions import Annotated
from models.models import User

security = HTTPBasic()

"""
def verification(
    creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    username = creds.username  # inputted username
    password = creds.password  # inputted password

    user = user_repo.get_user_by_username(db, username=username)
    if user == None:
        return False  # user does not exist
    return verify_password(password, user.hashed_password)
"""


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
        return jwt.login_for_access_token(username=username)
    else:
        raise unauthorized_exception


def get_current_user(creds: HTTPBasicCredentials = Depends(security)):
    return creds.username

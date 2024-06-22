from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from db.database import get_db
from db.repositories import user_repository as user_repo
from services.security import authenticate_user

security = HTTPBasic()


def verification(
    creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    username = creds.username  # inputted username
    password = creds.password  # inputted password

    user = user_repo.get_user_by_username(db, username=username)
    if user == None:
        return False  # user does not exist
    return authenticate_user(password, user.hashed_password)


def get_current_user(creds: HTTPBasicCredentials = Depends(security)):
    return creds.username

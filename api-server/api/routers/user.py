from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models.schemas import schemas
from db.database import get_db
from db.repositories import user_repository as user_repo


router = APIRouter(prefix="/user")
security = HTTPBasic()


def verification(
    creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    username = creds.username  # inputted username
    password = creds.password  # inputted password

    user = user_repo.get_user_by_username(db, username=username)
    if user == None:
        return False  # user does not exist
    return user_repo.authenticate_user(password, user.hashed_password)


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_repo.create_user(db=db, user=user)


@router.get("/test", response_model=List[schemas.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_repo.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/test?user_id={user_id}", response_model=schemas.User)
def read_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/login")
def login(Verification=Depends(verification)):
    if Verification:
        return {"message": "login succesful"}
    else:
        return HTMLResponse(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/unauthorize")
def unauthorize():
    return HTMLResponse(status_code=status.HTTP_401_UNAUTHORIZED)

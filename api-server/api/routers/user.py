from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models.schemas import user_schema
from db.database import get_db
from db.repositories import user_repository as user_repo
from services.auth import jwt
from typing_extensions import Annotated


router = APIRouter(prefix="/user")


@router.post("/create", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_repo.create_user(db=db, user=user)


@router.get("/test", response_model=List[user_schema.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_repo.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/test/list?user_id={user_id}", response_model=user_schema.User)
def read_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/unauthorize")
def unauthorize():
    return HTMLResponse(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/me")
async def read_users_me(
    current_user: Annotated[str, Depends(jwt.get_current_user)],
    db: Session = Depends(get_db),
):
    return user_repo.get_user_by_username(db, current_user)

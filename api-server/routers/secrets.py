from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import get_db


router = APIRouter(prefix="/secrets")
security = HTTPBasic()


def get_current_user(creds: HTTPBasicCredentials = Depends(security)):
    return creds.username


@router.post("/create")
def create_key(
    secret: schemas.SecretCreate,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    current_user_id = crud.get_user_by_username(db, current_user).id
    return crud.create_secret(db=db, secret=secret, user_id=current_user_id)


@router.get("/list")
def read_current_user_secrets(
    current_user: Session = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    current_user_id = crud.get_user_by_username(db, current_user).id
    return crud.get_secrets_by_user_id(
        db, user_id=current_user_id, skip=skip, limit=limit
    )


@router.get("/list?user_id={user_id}")
def read_secrets_by_user_id(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.get_secrets_by_user_id(db, user_id=user_id, skip=skip, limit=limit)


@router.delete("/secrets/delete?secret_id={secret_id}")
def delete_secret_by_id(secret_id: int, db: Session = Depends(get_db)):
    return crud.delete_secrets_by_id(db, secret_id)

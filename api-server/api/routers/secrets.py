from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from schemas import schemas
from db.database import get_db
from db.repositories import secrets_repository as secrets_repo
from db.repositories import user_repository as user_repo
from services.auth.jwt import get_current_user
from typing_extensions import Annotated
from models.models import User
from typing import List

router = APIRouter(prefix="/secrets")


@router.post("/create", response_model=schemas.Secret)
def create_key(
    current_user: Annotated[str, Depends(get_current_user)],
    secret: schemas.SecretCreate,
    db: Session = Depends(get_db),
):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    return secrets_repo.create_secret(db=db, secret=secret, user_id=current_user_id)


@router.get("/list", response_model=List[schemas.Secret])
def read_current_user_secrets(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return secrets_repo.get_secrets_by_user_id(db, user_id=user_id, skip=skip, limit=limit)


@router.delete("/delete")
def delete_secret_by_id(secret_id: int, db: Session = Depends(get_db)):
    deleted = secrets_repo.delete_secrets_by_id(db, secret_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"message": "Secret deleted successfully"}

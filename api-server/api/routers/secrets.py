from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.schemas import schemas
from db.database import get_db
from db.repositories import secrets_repository as secrets_repo
from db.repositories import user_repository as user_repo
from services.authentication import get_current_user


router = APIRouter(prefix="/secrets")


@router.post("/create")
def create_key(
    secret: schemas.SecretCreate,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    return secrets_repo.create_secret(db=db, secret=secret, user_id=current_user_id)


@router.get("/list")
def read_current_user_secrets(
    current_user: Session = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    return secrets_repo.get_secrets_by_user_id(
        db, user_id=current_user_id, skip=skip, limit=limit
    )


@router.get("/list?user_id={user_id}")
def read_secrets_by_user_id(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return secrets_repo.get_secrets_by_user_id(
        db, user_id=user_id, skip=skip, limit=limit
    )


@router.delete("/delete")
def delete_secret_by_id(secret_id: int, db: Session = Depends(get_db)):
    deleted = secrets_repo.delete_secrets_by_id(db, secret_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"message": "Secret deleted successfully"}

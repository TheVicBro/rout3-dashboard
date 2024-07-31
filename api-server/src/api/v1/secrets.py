from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.db.database import get_db
from app.db.repositories import secrets_repository as secrets_repo
from app.db.repositories import user_repository as user_repo
from app.schemas import secret_schema
from app.services.auth.jwt import get_current_user, verify_token

router = APIRouter(prefix="/secrets")


@router.post("/create", response_model=secret_schema.Secret)
def create_key(
    current_user: Annotated[str, Depends(get_current_user)],
    secret: secret_schema.SecretCreate,
    db: Session = Depends(get_db),
):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    return secrets_repo.create_secret(db=db, secret=secret, user_id=current_user_id)


@router.get("/list", response_model=List[secret_schema.Secret])
def read_current_user_secrets(
    verified_token: Annotated[str, Depends(verify_token)],
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    if verified_token:
        return secrets_repo.get_secrets_by_user_id(
            db, user_id=user_id, skip=skip, limit=limit
        )
    else:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")


@router.delete("/delete")
def delete_secret_by_id(
    secret_id: int,
    verified_token: Annotated[str, Depends(verify_token)],
    db: Session = Depends(get_db),
):
    if verified_token:
        deleted = secrets_repo.delete_secrets_by_id(db, secret_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Secret not found")
        return {"message": "Secret deleted successfully"}
    else:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")

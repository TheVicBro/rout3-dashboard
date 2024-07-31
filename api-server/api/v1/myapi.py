from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.db.database import get_db
from app.db.repositories import myapi_repository as myapi_repo
from app.db.repositories import user_repository as user_repo
from app.services import myapi
from app.services.auth.jwt import get_current_user

router = APIRouter(prefix="/api")


@router.post("/create_key")
def create_key(
    name: str,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    key = myapi.generate_api_key()
    myapi.key = key
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    return myapi_repo.create_myapi(
        db=db, myapi=myapi, user_id=current_user_id, name=name
    )


@router.get("/get_key_by_id")
def get_key_by_id(id: int, db: Session = Depends(get_db)):
    return myapi_repo.get_myapi_by_id(db, id)


@router.get("/get_key_by_user_id")
def get_key_by_user_id(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return myapi_repo.get_myapi_by_user_id(db, user_id, skip, limit)


# use this as a template to get api protected routes
@router.get("/test_protected")
def test_protected(
    api_key_header: str = Security(myapi.get_api_key_from_header),
    db: Session = Depends(get_db),
):
    api_key = myapi.verify_api_key(db=db, api_key_string=api_key_header)
    return "success"


@router.delete("/remove_key")
def remove_key(id: int, db: Session = Depends(get_db)):
    myapi_repo.remove_myapi(db, id)
    return "success"

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from db.database import get_db
from db.repositories import myapi_repository as myapi_repo
from services.jwt import get_current_user
from typing_extensions import Annotated
from services import myapi

router = APIRouter(prefix="/api")


@router.get("/get_key")
def get_key(
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    key = myapi.generate_api_key()
    myapi.key = key
    return myapi_repo.create_myapi(db=db, myapi=myapi, user_id=current_user)


# use this as a template to get api protected routes
@router.get("/test_protected")
def test_protected(
    api_key_header: str = Security(myapi.get_api_key_from_header),
    db: Session = Depends(get_db),
):
    api_key = myapi.verify_api_key(db=db, api_key_string=api_key_header)
    return "success"

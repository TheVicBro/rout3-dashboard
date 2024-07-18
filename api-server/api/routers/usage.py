from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import schemas
from db.database import get_db

from db.repositories import secrets_repository as secrets_repo
from db.repositories import user_repository as user_repo
from db.repositories import usage_repository as usage_repo

from services.auth.jwt import get_current_user
from typing_extensions import Annotated
from models.models import User
from typing import List

router = APIRouter(prefix="/usage")

@router.post("/create", response_model=schemas.Usage)
def record_usage():
    print("--------------------------------------WORKING TILL HERE----------------------------------------------")
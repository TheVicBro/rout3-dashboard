from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from services.myapi import verify_api_key
from schemas import schemas
from db.database import get_db
from db.repositories import user_repository as user_repo
from db.repositories import usage_repository as usage_repo

from services.auth.jwt import get_current_user
from errors.custom_db_errors import InvalidProvider, InvalidModel, InvalidDateRangeUsage

router = APIRouter(prefix="/usages")

@router.post("/create", response_model=schemas.UsageCreateData)
def record_usage(
    usage: schemas.UsageCreate,
    db: Session = Depends(get_db),
    ):
    try:
        verify_api_key(db, usage.api_key) # this method actually returns the key
        return {"data": usage_repo.create_usage_entry(db, usage), "error": "", "status": 200}
    except HTTPException as e:
        return {"data": {}, "error": e.detail, "status": e.status_code}


@router.get("/provider", response_model=schemas.UsageData)
def list_provider_usage(
    provider: str,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
    ):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    try:
        data = usage_repo.get_usage_by_provider(db, provider, user_id=current_user_id)
        return {"data": data, "error": "", "status": 200}
    except InvalidProvider as e:
        return {"data": [], "error": e.message, "status": e.status_code}


@router.get("/model", response_model=schemas.UsageData)
def list_model_usage(
    model: str,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
    ):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    try:
        data = usage_repo.get_usage_by_model(db, model, user_id=current_user_id)
        return {"data": data, "error": "", "status": 200}
    except InvalidModel as e:
        return {"data": [], "error": e.message, "status": e.status_code}


@router.get("/secret", response_model=schemas.UsageData)
def list_secret_usage(
    secret_id: int,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
    ):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    try:
        data = usage_repo.get_usage_by_secret(db, secret_id, current_user_id)
        return {"data": data, "error": "", "status": 200}
    except InvalidModel as e:
        return {"data": [], "error": e.message, "status": e.status_code}


@router.get("/date/range", response_model=schemas.UsageData)
def list_date_range_usage(
    start_date: datetime,
    end_date: datetime,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
    ):
    current_user_id = user_repo.get_user_by_username(db, current_user).id
    try:
        data = usage_repo.get_date_range_usage(db, start_date, end_date, current_user_id)
        return {"data": data, "error": "", "status": 200}
    except InvalidDateRangeUsage as e:
        return {"data": [], "error": e.message, "status": e.status_code}

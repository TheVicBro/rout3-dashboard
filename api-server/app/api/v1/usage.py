from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from typing_extensions import Optional
from app.services.myapi import verify_api_key
from app.schemas import UsageCreateData, UsageData, UsageCreate

from app.api.deps import UserDep, SessionDep
from app.repositories import usage_repo

router = APIRouter()


@router.post("/create", response_model=UsageCreateData)
def record_usage(
    db: SessionDep,
    usage: UsageCreate,
):
    verified = verify_api_key(db, usage.api_key)
    if verified:
        return usage_repo.create_usage_entry(db, usage)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@router.get("/model", response_model=UsageData)
def list_model_usage(
    db: SessionDep,
    user: UserDep,
    model: str,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
):
    data = usage_repo.get_usage_by_model(db, model, user.id, skip, limit)
    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data was not found",
        )
    else:
        return data


@router.get("/date/range", response_model=UsageData)
def list_date_range_usage(
    db: SessionDep,
    user: UserDep,
    start_date: datetime,
    end_date: datetime,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
):
    data = usage_repo.get_date_range_usage(
        db, start_date, end_date, user.id, skip, limit
    )
    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data was not found",
        )
    else:
        return data

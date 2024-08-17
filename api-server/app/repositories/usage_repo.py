from sqlalchemy.orm import Session
from app.schemas import UsageBase
from app.models import Usage
from datetime import datetime


def create_usage_entry(db: Session, usage: UsageBase):
    db_usage = Usage(
        model=usage.model,
        chat_history=usage.chat_history,
        prompt=usage.prompt,
        response=usage.response,
        prompt_cost=usage.prompt_cost,
        response_cost=usage.response_cost,
        prompt_tokens=usage.prompt_tokens,
        response_tokens=usage.response_tokens,
        date_time=usage.date_time,
        user_id=usage.user_id,
    )
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage


def get_usage_by_model(db: Session, model: str, user_id: int, skip: int, limit: int):
    db_usage = (
        db.query(Usage)
        .filter(Usage.user_id == user_id)
        .filter(Usage.model == model)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return db_usage


def get_date_range_usage(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    user_id: int,
    skip: int,
    limit: int,
):
    db_usage = (
        db.query(Usage)
        .filter(Usage.user_id == user_id)
        .filter(
            Usage.date_time > start_date,
            Usage.date_time < end_date,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return db_usage

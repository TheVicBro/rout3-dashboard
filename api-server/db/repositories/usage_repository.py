from sqlalchemy.orm import Session
from models import usage_model
from models.schemas import usage_schema 
from datetime import datetime
from errors.custom_db_errors import (
    InvalidProvider, 
    InvalidModel, 
    InvalidSecret, 
    InvalidDateRangeUsage
    )



def create_usage_entry(db: Session, usage: usage_schema.UsageBase):
    db_usage = usage_model.Usage(
                            provider=usage.provider,
                            model=usage.model,
                            chat_history=usage.chat_history,
                            prompt=usage.prompt,
                            response=usage.response,
                            input_cost=usage.input_cost,
                            prompt_cost=usage.prompt_cost,
                            response_cost=usage.response_cost,
                            prompt_tokens=usage.prompt_tokens,
                            response_tokens=usage.response_tokens,
                            date_time=usage.date_time,
                            user_id=usage.user_id,
                            secret_id=usage.secret_id
                            )
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage


def get_usage_by_provider(db: Session, provider: str, user_id: int, skip: int = 0, limit: int = 10):
    db_usage = ( 
        db.query(usage_model.Usage)
        .filter(usage_model.Usage.user_id == user_id)
        .filter(usage_model.Usage.provider == provider)
        .offset(skip)
        .limit(limit)
        .all()
    )
    if len(db_usage) == 0:
        raise InvalidProvider(provider)
    return db_usage


def get_usage_by_model(db: Session, model: str, user_id: int, skip: int = 0, limit: int = 10):
    db_usage = (
        db.query(usage_model.Usage)
        .filter(usage_model.Usage.user_id == user_id)
        .filter(usage_model.Usage.model == model)
        .offset(skip)
        .limit(limit)
        .all()
    )
    if len(db_usage) == 0:
        raise InvalidModel(model)
    return db_usage

def get_usage_by_secret(db: Session, secret_id: int, user_id: int, skip: int = 0, limit: int = 10):
    db_usage = ( 
        db.query(usage_model.Usage)
        .filter(usage_model.Usage.user_id == user_id)
        .filter(usage_model.Usage.secret_id == secret_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    if len(db_usage) == 0:
        raise InvalidSecret(secret_id)
    return db_usage

def get_date_range_usage(db: Session, start_date: datetime, end_date: datetime, user_id: int, skip: int = 0, limit: int = 7):
    db_usage = ( 
        db.query(usage_model.Usage)
        .filter(usage_model.Usage.user_id == user_id)
        .filter(usage_model.Usage.date_time > start_date, usage_model.Usage.date_time < end_date)
        .offset(skip)
        .limit(limit)
        .all()
    )
    if len(db_usage) == 0:
        raise InvalidDateRangeUsage(start_date, end_date)
    return db_usage

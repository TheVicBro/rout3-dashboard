from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models import Myapi


def create_myapi(db: Session, myapi_key: str, user_id: int, name: str):
    db_myapi = Myapi(key=myapi_key, user_id=user_id, name=name)
    db.add(db_myapi)
    db.commit()
    db.refresh(db_myapi)
    return db_myapi


def get_myapi(db: Session, key: str):
    myapi_key = db.query(Myapi).filter(Myapi.key == key).first()
    return myapi_key


def get_myapi_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Myapi).filter(Myapi.user_id == user_id).offset(skip).limit(limit).all()
    )


def get_myapi_by_id(db: Session, myapi_id: int, user_id: int):
    data = (
        db.query(Myapi)
        .filter(and_(Myapi.id == myapi_id, Myapi.user_id == user_id))
        .first()
    )
    return data


def remove_myapi(db: Session, myapi_id: int, user_id: int):
    # It will be successful no matter what
    data = (
        db.query(Myapi)
        .where(Myapi.user_id == user_id)
        .where(Myapi.id == myapi_id)
        .delete()
    )
    db.commit()
    return data


def get_user_id_by_myapi(db: Session, myapi_key: str):
    data = (
        db.query(Myapi)
        .filter(Myapi.key == myapi_key)
        .first()
    )
    db.commit()
    return data.user_id
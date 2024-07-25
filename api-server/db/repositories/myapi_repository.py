from sqlalchemy.orm import Session
from models import models
from schemas import schemas


def create_myapi(db: Session, myapi: schemas.MyApiCreate, user_id: int):
    # TODO: encrypt key
    fake_key = myapi.key
    db_myapi = models.Myapi(key=fake_key, user_id=user_id)
    db.add(db_myapi)
    db.commit()
    db.refresh(db_myapi)
    return db_myapi


def get_myapi(db: Session, key: str):
    return db.query(models.Myapi).filter(models.Myapi.key == key).first()


def get_myapi_by_user_id(db: Session, id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Myapi)
        .filter(models.Myapi.user_id == id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_myapi_by_id(db: Session, id: int):
    return db.query(models.Myapi).filter(models.Myapi.id == id).first()


def remove_myapi(db: Session, id: int):
    to_be_deleted = get_myapi_by_id(db, id)
    db.delete(to_be_deleted)
    db.commit()
    return {"message": "success"}

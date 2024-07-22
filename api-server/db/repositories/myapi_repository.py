from sqlalchemy.orm import Session
from models import models
from models.schemas import schemas


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

from sqlalchemy.orm import Session
from models import myapi_model
from models.schemas import myapi_schema


def create_myapi(db: Session, myapi: myapi_schema.MyApiCreate, user_id: int, name: str):
    # TODO: encrypt key
    fake_key = myapi.key
    db_myapi = myapi_model.Myapi(key=fake_key, user_id=user_id, name=name)
    db.add(db_myapi)
    db.commit()
    db.refresh(db_myapi)
    return db_myapi


def get_myapi(db: Session, key: str):
    return db.query(myapi_model.Myapi).filter(myapi_model.Myapi.key == key).first()


def get_myapi_by_user_id(db: Session, id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(myapi_model.Myapi)
        .filter(myapi_model.Myapi.user_id == id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_myapi_by_id(db: Session, id: int):
    return db.query(myapi_model.Myapi).filter(myapi_model.Myapi.id == id).first()


def remove_myapi(db: Session, id: int):
    to_be_deleted = get_myapi_by_id(db, id)
    db.delete(to_be_deleted)
    db.commit()
    return {"message": "success"}

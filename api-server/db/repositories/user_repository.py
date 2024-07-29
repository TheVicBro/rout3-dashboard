from sqlalchemy.orm import Session
from models import user_model
from models.schemas import user_schema
from services.auth.security import get_password_hash


def get_user_by_id(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return (
        db.query(user_model.User).filter(user_model.User.username == username).first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = user_model.User(
        username=user.username, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user_to_be_deleted = get_user_by_id(db, user_id)
    if user_to_be_deleted is None:
        raise Exception
    db.delete(user_to_be_deleted)
    db.commit()
    return {"message": "success"}

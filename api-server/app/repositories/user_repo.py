from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import User
from app.schemas import UserCreate


def get_user_by_id(db: Session, user_id: int):
    data = db.query(User).filter(User.id == user_id).first()
    return data


def get_user_by_username(db: Session, username: str):
    data = db.query(User).filter(User.username == username).first()
    return data


def get_user_by_email(db: Session, email: EmailStr):
    data = db.query(User).filter(User.email == email).first()
    return data


def get_users(db: Session, skip: int = 0, limit: int = 100):
    data = db.query(User).offset(skip).limit(limit).all()
    return data


def create_user(db: Session, user: UserCreate, is_admin: bool = False):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user_to_be_deleted = get_user_by_id(db, user_id)
    db.delete(user_to_be_deleted)
    db.commit()
    return {"message": "success"}

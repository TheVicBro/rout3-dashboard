from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

"""
user operations
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


"""
secrets operations
"""


def create_secret(db: Session, secret: schemas.SecretCreate, user_id: int):
    # TODO: encrypt key
    fake_key = secret.key
    db_secret = models.Secret(name=secret.name, key=fake_key, user_id=user_id)
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    return db_secret


def get_secrets_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Secret)
        .filter(models.Secret.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_secret_by_id(db: Session, secret_id: int):
    return db.query(models.Secret).filter(models.Secret.id == secret_id).first()


def delete_secrets_by_id(db: Session, id: int):
    to_be_deleted = get_secret_by_id(db, id)
    db.delete(to_be_deleted)
    db.commit()
    return {"message": "success"}

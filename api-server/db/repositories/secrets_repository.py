from sqlalchemy.orm import Session
from models import models
from schemas import schemas


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
    print("get secret")
    return db.query(models.Secret).filter(models.Secret.id == secret_id).first()


def delete_secrets_by_id(db: Session, id: int):
    print("delete secret")
    to_be_deleted = get_secret_by_id(db, id)
    db.delete(to_be_deleted)
    db.commit()
    return {"message": "success"}

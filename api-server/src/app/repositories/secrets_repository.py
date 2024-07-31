from sqlalchemy.orm import Session

from app.models import secret_model
from app.schemas import secret_schema


def create_secret(db: Session, secret: secret_schema.SecretCreate, user_id: int):
    # TODO: encrypt key
    fake_key = secret.key
    db_secret = secret_model.Secret(
        name=secret.name, key=fake_key, user_id=user_id, last_used=secret.last_used
    )
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    return db_secret


def get_secrets_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(secret_model.Secret)
        .filter(secret_model.Secret.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_secret_by_id(db: Session, secret_id: int):
    print("get secret")
    return (
        db.query(secret_model.Secret)
        .filter(secret_model.Secret.id == secret_id)
        .first()
    )


def delete_secrets_by_id(db: Session, id: int):
    print("delete secret")
    to_be_deleted = get_secret_by_id(db, id)
    db.delete(to_be_deleted)
    db.commit()
    return {"message": "success"}

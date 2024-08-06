from sqlalchemy.orm import Session

from app.models import Secret
from app.schemas import Message, SecretCreate
from app.core import security


def create_secret(db: Session, secret: SecretCreate, user_id: int) -> Secret | None:
    encrypted_key = security.encrypt_data(secret.key)
    secret_obj = Secret(
        name=secret.name, key=encrypted_key, user_id=user_id, last_used=secret.last_used
    )
    db.add(secret_obj)
    db.commit()
    db.refresh(secret_obj)
    return secret_obj


def get_secrets_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    data = (
        db.query(Secret)
        .filter(Secret.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return data


def delete_secrets_by_id(db: Session, id: int):
    to_be_deleted = db.get(Secret, id)

    if to_be_deleted:
        db.delete(to_be_deleted)
        db.commit()
        return Message(message="Item successfully deleted")
    return None

from sqlalchemy.orm import Session
from models import models
from schemas import schemas

def create_usage_entry(db: Session, usage: schemas.Usage, user_id: str, secrets_id: str):
    db_usage = models.Usage(model=usage.model, cost=usage.cost, token=usage.token, date_time=usage.date_time, 
                            user_id=user_id, provider=usage.provider, secrets_id=secrets_id)
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage
    
def get_usage_by_provider(db: Session, provider: str, skip: int = 0, limit: int = 0):
    return( 
        db.query(models.Usage)
        .filter(models.Usage.provider == provider)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_usage_by_model(db: Session, model: str, , skip: int = 0, limit: int = 0):
    return( 
        db.query(models.Usage)
        .filter(models.Usage.model == model)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_usage_by_secret(db: Session, secret_id: int, , skip: int = 0, limit: int = 0):
    return( 
        db.query(models.Usage)
        .filter(models.Usage.secrets_id == secret_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

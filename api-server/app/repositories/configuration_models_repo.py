from sqlalchemy.orm import Session

from app.models import Config_Models


# create configuration
def create_config_models(
    db: Session,
    config_id: int,
    secret_key: str,
    models: str,
    max_tokens: int,
    temperature: float,
):
    db_config_model = Config_Models(
        config_id=config_id,
        secret_key=secret_key,
        models=models,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    db.add(db_config_model)
    db.commit()
    db.refresh(db_config_model)
    return db_config_model


# update configuration
def update_config_models(
    db: Session, config_model_id: int, models: str, max_tokens: int, temperature: float
):
    db_config_model = (
        db.query(Config_Models).filter(Config_Models.id == config_model_id).first()
    )

    # update only given parameters
    if models is not None:
        db_config_model.models = models
    if max_tokens is not None:
        db_config_model.max_tokens = max_tokens
    if temperature is not None:
        db_config_model.temperature = temperature

    db.commit()
    db.refresh(db_config_model)
    return db_config_model


# get configuration models by id
def get_configuration_models_by_id(db: Session, config_models_id: int):
    data = db.query(Config_Models).filter(Config_Models.id == config_models_id).first()
    return data


# get all configuration models by configuration id
def get_configuration_models_by_config_id(
    db: Session, config_id: int, skip: int = 0, limit: int = 10
):
    data = (
        db.query(Config_Models)
        .filter(Config_Models.config_id == config_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return data


# delete model
def delete_config_model(db: Session, config_model_id: int):
    # It will be successful no matter what
    data = db.query(Config_Models).where(Config_Models.id == config_model_id).delete()
    db.commit()
    return data

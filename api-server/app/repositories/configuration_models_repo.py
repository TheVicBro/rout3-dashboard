from sqlalchemy.orm import Session

from app.models import Config_Model


# create configuration
def create_config_model(
    db: Session,
    config_id: int,
    secret_key: str,
    model: str,
    max_tokens: int,
    temperature: float,
):
    db_config_model = Config_Model(
        config_id=config_id,
        secret_key=secret_key,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    db.add(db_config_model)
    db.commit()
    db.refresh(db_config_model)
    return db_config_model


# update configuration
def update_config_model(
    db: Session, config_model_id: int, model: str, max_tokens: int, temperature: float
):
    db_config_model = (
        db.query(Config_Model).filter(Config_Model.id == config_model_id).first()
    )

    # update only given parameters
    if model is not None:
        db_config_model.model = model
    if max_tokens is not None:
        db_config_model.max_tokens = max_tokens
    if temperature is not None:
        db_config_model.temperature = temperature

    db.commit()
    db.refresh(db_config_model)
    return db_config_model


# get configuration model by id
def get_configuration_model_by_id(db: Session, config_model_id: int):
    data = db.query(Config_Model).filter(Config_Model.id == config_model_id).first()
    return data


# get all configuration model by configuration id
def get_configuration_model_by_config_id(
    db: Session, config_id: int, skip: int = 0, limit: int = 10
):
    data = (
        db.query(Config_Model)
        .filter(Config_Model.config_id == config_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return data


# delete model
def delete_config_model(db: Session, config_model_id: int):
    # It will be successful no matter what
    data = db.query(Config_Model).where(Config_Model.id == config_model_id)
    model = data.first().model
    data.delete()
    db.commit()
    return model

from sqlalchemy.orm import Session

from app.models import Config


# create configuration
def create_config(db: Session, route_type: str, timeout: int):
    db_config = Config(route_type=route_type, timeout=timeout)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


# update configuration
def update_configuration(db: Session, config_id: int, route_type: str, timeout: int):
    db_config = db.query(Config).filter(Config.id == config_id).first()

    # update only given parameters
    if route_type is not None:
        db_config.route_type = route_type
    if timeout is not None:
        db_config.timeout = timeout

    db.commit()
    db.refresh(db_config)


# get configuration by id
def get_configuration_by_id(db: Session, config_id: int):
    data = db.query(Config).filter(Config.config_id == config_id).first()
    return data


# get all configurations for a user
def get_configuration_by_user_id(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
):
    return (
        db.query(Config)
        .filter(Config.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

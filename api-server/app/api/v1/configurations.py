from fastapi import APIRouter, HTTPException, Security, status
from fastapi.responses import JSONResponse

from app.api.deps import SessionDep, UserDep
from app.repositories import (
    configurations_repo,
    configuration_models_repo,
    secrets_repo,
)
from app.schemas import (
    Configuration,
    ConfigBase,
    ConfigBase,
    ConfigModel,
    ConfigModelBase,
    ConfigModelKey,
)
from app.core import security

router = APIRouter()

"""Base Configurations"""


@router.post("/", response_model=Configuration)
def create_configuration(config_data: ConfigBase, db: SessionDep, user: UserDep):
    """
    Create new configuration setup.
    One record per user.
    """
    try:
        config = configurations_repo.create_config(
            db=db,
            user_id=user.id,
            route_type=config_data.route_type,
            timeout=config_data.timeout,
        )
        return config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Failed to create configuration record",
        )


@router.post("/edit", response_model=ConfigBase)
def edit_configuration(config_update_data: ConfigBase, db: SessionDep, user: UserDep):
    """
    Edit existing configurations.
    Can only edit router_name and timeout parameters.
    """
    try:
        config_updated = configurations_repo.update_configuration(
            db=db,
            user_id=user.id,
            route_type=config_update_data.route_type,
            timeout=config_update_data.timeout,
        )
        return config_updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to reset configuration record",
        )


@router.patch("/reset", response_model=ConfigBase)
def reset_configuration(db: SessionDep, user: UserDep):
    """
    Reset configurations to default values
    """
    try:
        config_updated = configurations_repo.update_configuration(
            db=db,
            user_id=user.id,
            route_type="cost",
            timeout=1,
        )
        return config_updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to reset configuration record",
        )


@router.get("/", response_model=Configuration)
def get_configuration(db: SessionDep, user: UserDep):
    """
    Get configuration setup for the current user
    """
    try:
        config = configurations_repo.get_configuration_by_user_id(db, user.id)
        return config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to get current user's configuration record",
        )


"""Configuration Models"""


@router.post("/model", response_model=ConfigModel)
def create_configuration_model(
    config_model_data: ConfigModelBase, secret_id: int, db: SessionDep, user: UserDep
):
    """
    Create a new configuration model record.
    Multiple records can exist for each configuration/user
    """
    try:
        secret = secrets_repo.get_secret_by_id(db, secret_id)
        config = configurations_repo.get_configuration_by_user_id(db, user.id)
        config_model = configuration_models_repo.create_config_models(
            db=db,
            config_id=config.id,
            secret_key=secret.key,
            models=config_model_data.models,
            max_tokens=config_model_data.max_tokens,
            temperature=config_model_data.temperature,
        )
        return config_model
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Failed to create configuration model record",
        )


@router.post("/model/edit", response_model=ConfigBase)
def edit_configuration_model(
    config_model_data: ConfigModelBase,
    config_model_id: int,
    db: SessionDep,
):
    """
    Edit existing configurations.
    Can only edit models, max tokens, and temperature parameters.
    """
    try:
        config_model_updated = configuration_models_repo.update_config_models(
            db=db,
            config_model_id=config_model_id,
            models=config_model_data.models,
            max_tokens=config_model_data.max_tokens,
            temperature=config_model_data.temperature,
        )
        return config_model_updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to reset configuration model record",
        )


@router.patch("/model/reset", response_model=ConfigModelBase)
def reset_configuration_model(
    config_model_id: int,
    db: SessionDep,
):
    """
    Reset configuration model to default values
    """
    try:
        config_model_updated = configuration_models_repo.update_config_models(
            db=db,
            config_model_id=config_model_id,
            models=None,
            max_tokens=512,
            temperature=0.75,
        )
        return config_model_updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to reset configuration model record",
        )


@router.get("/model/", response_model=ConfigModel)
def get_configuration_model_by_id(
    db: SessionDep,
    config_models_id: int,
):
    """
    Get configuration model setup by id
    """
    try:
        config_model = configuration_models_repo.get_configuration_models_by_id(
            db, config_models_id=config_models_id
        )
        return config_model
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to get a configuration model record",
        )


@router.get("/model/{config_id}/", response_model=list[ConfigModel])
def get_configuratio_model_by_config_id(
    config_id: int,
    db: SessionDep,
):
    """
    Get all configuration models from the current user's configuration
    """
    try:
        config_model = configuration_models_repo.get_configuration_models_by_config_id(
            db, config_id=config_id
        )
        return config_model
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to get all configuration models",
        )


@router.get("/key/{config_id}")
def get_configuration_by_id(db: SessionDep, config_models_id: int):
    """
    Get model secret key and decrypt it
    """
    try:
        config_model = configuration_models_repo.get_configuration_models_by_id(
            db, config_models_id=config_models_id
        )
        key = security.fernet_decrypt_data(config_model.secret_key)
        return key
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to get a secret key",
        )


@router.delete("/model/{config_model_id}")
def remove_config_model_record(config_models_id: int, db: SessionDep):
    """
    Delete a configuration model record
    """
    try:
        config_model = configuration_models_repo.delete_config_model(
            db, config_models_id=config_models_id
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Configuration Model successfully deleted",
                "model": config_model.models,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to delete configuration model",
        )

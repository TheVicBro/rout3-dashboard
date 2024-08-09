from fastapi import APIRouter, HTTPException, Security, status
from fastapi.responses import JSONResponse

from app.api.deps import SessionDep, UserDep
from app.repositories import configurations_repo, configuration_models_repo
from app.schemas import (
    Configuration,
    ConfigBase,
    ConfigBase,
    ConfigModel,
    ConfigModelBase,
    ConfigModelKey,
)

router = APIRouter()

"""Base Configurations"""


@router.post("/", response_model=Configuration)
def create_configuration(config_data: ConfigBase, db: SessionDep, user: UserDep):
    """
    Create new configuration setup.
    One record per user.
    """
    try:
        config_model = configurations_repo.create_config(
            db=db,
            user_id=user.id,
            route_type=config_data.route_type,
            timeout=config_data.timeout,
        )
        return config_model
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
        config_model_updated = configurations_repo.update_configuration(
            db=db,
            user_id=user.id,
            route_type=config_update_data.route_type,
            timeout=config_update_data.timeout,
        )
        return config_model_updated
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
        config_model_updated = configurations_repo.update_configuration(
            db=db,
            user_id=user.id,
            route_type="cost",
            timeout=1,
        )
        return config_model_updated
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
        config_model = configurations_repo.get_configuration_by_user_id(db, user.id)
        return config_model
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to get current user's configuration record",
        )


"""Configuration Models"""


# @router.post("/", response_mode=Config)
# def create_configuration(
#     db: SessionDep,
# ):
#     return None


# @router.post("/edit", response_model=ConfigBase)
# def edit_configuration(
#     db: SessionDep,
# ):
#     return None


# @router.patch("/reset", response_model=Config)
# def reset_configuration(
#     db: SessionDep,
# ):
#     return None


# @router.get("/", response_model=Config)
# def get_configuration_by_id(
#     db: SessionDep,
# ):
#     return None


# @router.get("/{config_id}/", response_model=list[Config])
# def get_configuration_by_id(
#     db: SessionDep,
# ):
#     return None


# @router.get("/key/{config_id}", response_model=ConfigModelKey)
# def get_configuration_by_id(
#     db: SessionDep,
# ):
#     return None

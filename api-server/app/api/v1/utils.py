from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import User, Config

router = APIRouter()


@router.get("/all_users")
def get_all_users(db: SessionDep):
    # Just doing it directly here for the util code
    users = db.query(User).all()
    return users


@router.get("/all_configss")
def get_all_configurations(db: SessionDep):
    configurations = db.query(Config).all()
    return configurations

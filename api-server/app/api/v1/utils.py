from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import User

router = APIRouter()


@router.get("/all_users")
def get_all_users(db: SessionDep):
    # Just doing it directly here for the util code
    users = db.query(User).all()
    return users

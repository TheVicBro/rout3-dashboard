from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.repositories import user_repo
from app.schemas import User, UserCreate

router = APIRouter()


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: SessionDep):
    # NOTE: We should be getting by email or uuid, but this should work for now
    db_user = user_repo.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username is already registered!")
    # For later
    is_admin = False
    return user_repo.create_user(db=db, user=user, is_admin=is_admin)


# TODO protect with admin account credentials
# DELETE IN DB directly for now
# @router.delete("/delete")
# def delete_user_by_id(
#     user_id: str,
#     verified_token: Annotated[str, Depends(jwt.verify_token)],
#     db: Session = Depends(get_db),
# ):
#     if verified_token:
#         deleted = user_repo.delete_secrets_by_id(db, user_id)
#         if not deleted:
#             raise HTTPException(status_code=404, detail="User not found")
#         return {"message": "User deleted successfully"}
#     else:
#         aise HTTPException(status_code=401, detail="Could not validate credentials.")

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep, UserDep
from app.repositories import secrets_repo
from app.schemas import Secret, SecretCreate

router = APIRouter()


@router.post("/", response_model=Secret)
def add_secret(
    db: SessionDep,
    user: UserDep,
    secret: SecretCreate,
):
    """
    Add secret to current user
    """
    # Fix type error later, still works for now
    try:
        return secrets_repo.create_secret(db=db, secret=secret, user_id=user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Failed to create secret.",
        ) from e


# Later we can create a super users that can get all secrets in an org for example
# We do not use user_id as malicious users can take advatage of this; jwt is more secure when ensuring that it is a valid user
@router.get("/", response_model=List[Secret])
def read_current_user_secrets(
    db: SessionDep,
    user: UserDep,
    skip: int = 0,
    limit: int = 10,
):
    """
    Get current users secrets
    """
    return secrets_repo.get_secrets_by_user_id(
        db, user_id=user.id, skip=skip, limit=limit
    )


# Todo: Make availble with super user
# @router.delete("/delete")
# def delete_secret_by_id(
#     secret_id: int,
#     verified_token: Annotated[str, Depends(verify_token)],
#     db: Session = Depends(get_db),
# ):
#     if verified_token:
#         deleted = secrets_repo.delete_secrets_by_id(db, secret_id)
#         if not deleted:
#             raise HTTPException(status_code=404, detail="Secret not found")
#         return {"message": "Secret deleted successfully"}
#     else:
#         raise HTTPExeption(status_code=401, detail="Could not validate credentials.")

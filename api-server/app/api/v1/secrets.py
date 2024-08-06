from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.deps import SessionDep, UserDep, require_auth
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
    res = secrets_repo.create_secret(db=db, secret=secret, user_id=user.id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Failed to add secret. Please ensure the key is unique.",
        )

    return res


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


@router.delete("/{secret_id}", dependencies=[require_auth])
def delete_secret_by_id(secret_id: int, db: SessionDep):
    """
    Delete Secret of current user using secret_id in DB.
    """
    res = secrets_repo.delete_secrets_by_id(db, secret_id)

    if res:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": res.message}
        )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
       detail="Secret not delete. Please ensure id exists.",
    )

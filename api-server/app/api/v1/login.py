from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from app.api.deps import SessionDep
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas import Token
from app.services.auth import authenticate_user

router = APIRouter()


@router.post("/login/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    Must have existing username and valid matching password
    """

    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = authenticate_user(
        db=db, username=form_data.username, plain_password=form_data.password
    )

    if not user:
        raise unauthorized_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return create_access_token(sub=str(user.id), expires_delta=access_token_expires)

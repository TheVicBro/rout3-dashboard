from fastapi import APIRouter, HTTPException, Security, status
from fastapi.responses import JSONResponse

from app.api.deps import SessionDep, UserDep
from app.repositories import myapi_repo
from app.schemas import Myapi, MyApiBase
from app.services import myapi

router = APIRouter()


@router.post("/", response_model=Myapi)
def create_api_key(
    myapi_data: MyApiBase,
    user: UserDep,
    db: SessionDep,
):
    """
    Create new myapi for user to connect to unified interface
    """
    virtual_key = myapi.generate_api_key()
    return myapi_repo.create_myapi(
        db=db, myapi_key=virtual_key, user_id=user.id, name=myapi_data.name
    )


@router.get("/", response_model=list[Myapi])
def get_user_myapi_keys(
    db: SessionDep,
    user: UserDep,
    skip: int = 0,
    limit: int = 10,
):
    """Get Current User's myapi_keys"""

    try:
        return myapi_repo.get_myapi_by_user_id(
            db=db, user_id=user.id, skip=skip, limit=limit
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to get current user's myapi.",
        )


@router.get("/{myapi_key_id}/", response_model=Myapi)
def get_key_by_id(myapi_key_id: int, db: SessionDep, user: UserDep):
    # We need to use if statement where, as the db returns null, rather than throwing an exeception
    data = myapi_repo.get_myapi_by_id(db=db, myapi_id=myapi_key_id, user_id=user.id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to get current user's myapi.",
        )

    return data


@router.delete("/{myapi_key_id}")
def remove_key(myapi_key_id: int, db: SessionDep, user: UserDep):
    data = myapi_repo.remove_myapi(db, myapi_key_id, user_id=user.id)
    if data == 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to remove myapi_key.",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Key successfully deleted"}
    )


# use this as a template to get api protected routes
@router.get("/test_protected")
def test_protected(
    db: SessionDep,
    api_key_header: str = Security(myapi.get_api_key_from_header),
):
    myapi.verify_api_key(db=db, api_key_string=api_key_header)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Key successfully deleted."
    )

from fastapi import APIRouter

from app.api.v1 import login, myapi, secrets, user

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(secrets.router, prefix="/secrets", tags=["secrets"])
api_router.include_router(myapi.router, prefix="/myapi", tags=["myapi"])

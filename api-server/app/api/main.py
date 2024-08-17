from fastapi import APIRouter

from app.api.v1 import login, myapi, secrets, user, utils, router, configurations, usage


api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(secrets.router, prefix="/secrets", tags=["secrets"])
api_router.include_router(myapi.router, prefix="/myapi", tags=["myapi"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(router.router, prefix="/router", tags=["router"])
api_router.include_router(
    configurations.router, prefix="/config", tags=["configuration"]
)
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])

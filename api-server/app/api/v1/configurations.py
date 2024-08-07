from fastapi import APIRouter, HTTPException, Security, status
from fastapi.responses import JSONResponse

from app.api.deps import SessionDep, UserDep
from app.repositories import myapi_repo
from app.schemas import Myapi, MyApiBase
from app.services import myapi
from app.core import security

router = APIRouter()

# create (POST)
@router.post("/create")

# update (PUT)
@router.post("/edit")

# reset (PATCH)
@router.patch("/reset")

# list user configs (GET)
@router.get("/{config_id}/")

import secrets

from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
users endpoints
"""


@app.post("/users/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/test/", response_model=List[schemas.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/test?user_id={user_id}", response_model=schemas.User)
def read_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def verification(
    creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    username = creds.username  # inputted username
    password = creds.password  # inputted password

    user = crud.get_user_by_username(db, username=username)
    if user == None:
        return False  # user does not exist
    if user.hashed_password == password:
        return True

    return False  # password incorrect


@app.get("/users/login")
async def login(Verification=Depends(verification)):
    if Verification:
        return {"message": "login succesful"}
    else:
        return HTMLResponse(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post("/users/unauthorize")
async def unauthorize():
    return HTMLResponse(status_code=status.HTTP_401_UNAUTHORIZED)


"""
secrets endpoints
"""


def get_current_user(creds: HTTPBasicCredentials = Depends(security)):
    return creds.username


@app.post("/secrets/create")
async def create_key(
    secret: schemas.SecretCreate,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    current_user_id = crud.get_user_by_username(db, current_user).id
    return crud.create_secret(db=db, secret=secret, user_id=current_user_id)


@app.get("/secrets/list/")
def read_secrets_by_user_id(
    current_user: Session = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    current_user_id = crud.get_user_by_username(db, current_user).id
    return crud.get_secrets_by_user_id(
        db, user_id=current_user_id, skip=skip, limit=limit
    )


@app.delete("/secrets/{secret_id}")
def delete_secret_by_id(secret_id: int, db: Session = Depends(get_db)):
    return crud.delete_secrets_by_id(db, secret_id)

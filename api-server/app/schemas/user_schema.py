from typing import List

from pydantic import BaseModel

from app.schemas.secret_schema import Secret


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    """
    Seperate password from base model
    so it won't be sent from API when reading a user
    """

    password: str


class User(UserBase):
    id: int
    secrets: List[Secret] = []

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import List, Optional


class SecretBase(BaseModel):
    provider: str
    last_used: str


class SecretCreate(SecretBase):
    """
    Seperate key from base model
    so it won't be sent from API when reading a secrets
    """
    key: str


class Secret(SecretBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


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


class MyApiBase(BaseModel):
    id: int
    user_id: int


class MyApiCreate(MyApiBase):
    key: str

class UsageBase(BaseModel):
    model: str
    cost: float
    token: int
    provider: str
    date_time: str
    
class Usage(UsageBase):
    id: int
    user_id: int
    secret_id: int
    class Config:
        orm_mode: True

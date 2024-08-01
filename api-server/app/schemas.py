from typing import List

from pydantic import BaseModel


# Secret Schemas
class SecretBase(BaseModel):
    name: str
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


# User Schemas
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
    hashed_password: str

    class Config:
        orm_mode = True


# My API Schemas
class MyApiBase(BaseModel):
    name: str


class MyApiCreate(MyApiBase):
    key: str


class Myapi(MyApiBase):
    id: int
    user_id: int


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str = ""
    exp: int


# General Schemas
class Message(BaseModel):
    message: str

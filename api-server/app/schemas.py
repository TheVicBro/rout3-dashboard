from datetime import datetime
from typing import List, Dict, Literal

from pydantic import BaseModel, EmailStr


# Secret Schemas
class SecretBase(BaseModel):
    name: str
    last_used: datetime


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


# My API Schemas
class MyApiBase(BaseModel):
    name: str


class MyApiCreate(MyApiBase):
    key: str


class Myapi(MyApiBase):
    id: int
    user_id: int
    key: str


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


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


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
    is_admin: bool
    myapi: List[Myapi]

    class Config:
        orm_mode = True


class RouteRequest(BaseModel):
    chat_history: List[Dict[str, str]]


# Configuration Schemas


class ConfigBase(BaseModel):
    timeout: int
    route_type: Literal["cost"]


class Configuration(ConfigBase):
    id: int
    router_name: str
    user_id: int

    class Config:
        orm_mode = True


# Configuration Model Schemas


class ConfigModelBase(BaseModel):
    model: str
    max_tokens: int
    temperature: float


class ConfigModel(ConfigModelBase):
    id: int
    config_id: int


class ConfigModelKey(ConfigModelBase):
    key: str

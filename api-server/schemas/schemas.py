from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime


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
    user_id: int
    secret_id: int
    provider: str
    model: str
    prompt: str
    response: str
    chat_history: List[Dict[str, str]]
    date_time: datetime
    input_cost: float
    prompt_cost: float
    response_cost: float
    prompt_tokens: int
    response_tokens: int


class UsageCreate(UsageBase):
    api_key: str


class Usage(UsageBase):
    id: int


class UsageData(BaseModel):
    data: List[Usage]
    error: str
    status: int

    class Config:
        orm_mode = True


class UsageCreateData(BaseModel):
    data: Usage | Dict
    error: str
    status: int

    class Config:
        orm_mode = True

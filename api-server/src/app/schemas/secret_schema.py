from pydantic import BaseModel
from typing import Optional


class SecretBase(BaseModel):
    name: str


class SecretCreate(SecretBase):
    """
    Seperate key from base model
    so it won't be sent from API when reading a secrets
    """

    key: str
    last_used: Optional[str] = None


class Secret(SecretBase):
    id: int
    last_used: Optional[str] = None
    user_id: int

    class Config:
        orm_mode = True

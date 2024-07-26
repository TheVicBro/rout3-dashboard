from pydantic import BaseModel


class MyApiBase(BaseModel):
    id: int
    user_id: int


class MyApiCreate(MyApiBase):
    key: str

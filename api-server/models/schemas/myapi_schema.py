from pydantic import BaseModel


class MyApiBase(BaseModel):
    id: int
    user_id: int
    name: str


class MyApiCreate(MyApiBase):
    key: str

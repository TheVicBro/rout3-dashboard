from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

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
    data: Usage|Dict
    error: str
    status: int
    
    class Config:
        orm_mode = True
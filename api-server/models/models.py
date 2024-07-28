from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    userid: int | None = None


class TokenData(BaseModel):
    username: str | None = None


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # is_active = Column(Boolean, default=True)

    secrets = relationship("Secret", back_populates="user")
    myapi = relationship("Myapi", back_populates="user")


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False)  
    last_used = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="secrets")
    usages = relationship("Usage", back_populates="secret")
    # usages = relationship("Usage", back_populates="secret", cascade="all, delete-orphan")


class Usage(Base):
    __tablename__= "usages"

    id = Column(Integer, primary_key=True)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    chat_history = Column(JSON, nullable=False)
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    input_cost = Column(Float, nullable=False) # We will need to update the proxy tokenizer to tokenize the chat_history too in order to grab this cost
    prompt_cost = Column(Float, nullable=False)
    response_cost = Column(Float, nullable=False)
    prompt_tokens = Column(Integer, nullable=False)
    response_tokens = Column(Integer, nullable=False)
    date_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    secret_id = Column(Integer, ForeignKey("secrets.id"))
    
    secret = relationship("Secret", back_populates="usages")


class Myapi(Base):
    __tablename__ = "myapi"

    id = Column(Integer, primary_key=True)
    key = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="myapi")

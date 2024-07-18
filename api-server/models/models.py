from typing import Union
from sqlalchemy import Column, Integer, String, Float, ForeignKey
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


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True)
    provider = Column(String, nullable=False)
    key = Column(String, nullable=False)
    last_used = Column(String, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="secrets")
    usages = relationship("Usage", back_populates="secret", cascade="all, delete-orphan")


class Usage(Base):
    __tablename__= "usage"
    
    id= Column(Integer, primary_key=True)
    model = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    tokens = Column(Integer, nullable=False)
    date_time = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    secrets_id = Column(Integer, ForeignKey("secrets.id"))
    secret = relationship("Secret", back_populates="usages")

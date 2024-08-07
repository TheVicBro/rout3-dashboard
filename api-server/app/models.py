from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class Myapi(Base):
    __tablename__ = "myapi"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    key = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="myapi")


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String, unique=True)
    last_used = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="secrets")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    email = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    secrets = relationship("Secret", back_populates="user")
    myapi = relationship("Myapi", back_populates="user")
    configuration = relationship("Config", back_populates="user")


class Config(Base):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True)
    provider = Column(String, index=True)  # scrap
    model = Column(String)  # enums
    max_tokens = Column(Integer)
    temperature = Column(Float)
    route_type = Column(String, index=True)  # enums
    timeout = Column(Integer)
    force_timeout = Column(Boolean, default=False)
    secrets_id = Column(Integer, ForeignKey("secrets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="configuration")

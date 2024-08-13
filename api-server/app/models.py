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
    timeout = Column(Integer, default=1)
    route_type = Column(String, nullable=False, index=True, default="cost")  # enums
    router_name = Column(String, default="router")  # DO NOT CHANGE
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,  # allow only one record per user to exist in the database
    )
    user = relationship("User", back_populates="configuration")
    config_model = relationship("Config_Model", back_populates="configuration")


class Config_Model(Base):
    __tablename__ = "config_model"

    id = Column(Integer, primary_key=True)
    config_id = Column(Integer, ForeignKey("configuration.id"))
    secret_key = Column(String, ForeignKey("secrets.key"))
    model = Column(String)
    max_tokens = Column(Integer, nullable=False, default=512)
    temperature = Column(Float, nullable=False, default=0.75)

    configuration = relationship("Config", back_populates="config_model")

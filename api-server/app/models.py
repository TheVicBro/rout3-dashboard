from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Myapi(Base):
    __tablename__ = "myapi"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="myapi")


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)
    last_used = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="secrets")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)

    secrets = relationship("Secret", back_populates="user")
    myapi = relationship("Myapi", back_populates="user")

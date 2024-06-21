from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)

    secrets = relationship("Secret", back_populates="user")


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)
    last_used = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="secrets")

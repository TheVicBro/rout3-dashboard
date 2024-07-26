from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)

    secrets = relationship("Secret", back_populates="user")
    myapi = relationship("Myapi", back_populates="user")

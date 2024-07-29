from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from models.user_model import User 

class Myapi(Base):
    __tablename__ = "myapi"

    id = Column(Integer, primary_key=True)
    key = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="myapi")

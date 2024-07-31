from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Myapi(Base):
    __tablename__ = "myapi"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="myapi")

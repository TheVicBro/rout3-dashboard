from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)
    last_used = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="secrets")

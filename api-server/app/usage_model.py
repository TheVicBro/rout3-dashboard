from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Usage(Base):
    __tablename__= "usages"

    id = Column(Integer, primary_key=True)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    chat_history = Column(JSON, nullable=False)
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    input_cost = Column(Float, nullable=False)
    prompt_cost = Column(Float, nullable=False)
    response_cost = Column(Float, nullable=False)
    prompt_tokens = Column(Integer, nullable=False)
    response_tokens = Column(Integer, nullable=False)
    date_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    secret_id = Column(Integer, ForeignKey("secrets.id"))
    
    secret = relationship("Secret", back_populates="usages")
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    blocked = Column(Boolean, default=False)
    blocked_at = Column(DateTime, nullable=True)
    mention_count = Column(Integer, default=0)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    content = Column(String)
    result = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

"""
User Model
"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    department = Column(String(100))
    role = Column(String(50))  # Admin, Auditor, Auditee, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

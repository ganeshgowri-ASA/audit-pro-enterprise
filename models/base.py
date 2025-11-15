"""
Base Model
AuditPro Enterprise - Common fields and methods for all models
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from config.database import Base


class BaseModel(Base):
    """
    Abstract base model with common fields
    All models should inherit from this class
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """
        Convert model to dictionary
        Useful for JSON serialization
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result

    def __repr__(self):
        """String representation of model"""
        return f"<{self.__class__.__name__}(id={self.id})>"

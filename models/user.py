"""
User model for authentication and authorization.
Implements role-based access control (RBAC) for the audit management system.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    """
    User model for authentication and authorization.

    Roles:
    - admin: Full access to all features
    - auditor: Create audits, view all data, manage findings
    - auditee: View assigned audits, respond to findings
    - viewer: Read-only access to audits and reports
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, auditor, auditee, viewer
    full_name = Column(String(100))
    department = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}', active={self.is_active})>"

    def to_dict(self):
        """Convert user object to dictionary (excluding password hash)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'full_name': self.full_name,
            'department': self.department,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

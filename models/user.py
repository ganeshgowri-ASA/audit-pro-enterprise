"""
User Model
AuditPro Enterprise - User authentication and management
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
import bcrypt
from models.base import BaseModel


class User(BaseModel):
    """
    User model for authentication and access control
    """
    __tablename__ = "users"

    # User credentials
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # User profile
    full_name = Column(String(100), nullable=False)
    employee_id = Column(String(50), unique=True)
    department = Column(String(100))
    role = Column(String(50), nullable=False, default="User")  # Admin, Auditor, Quality Manager, Department Head, User

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_auditor = Column(Boolean, default=False, nullable=False)

    # Relationships
    audits_conducted = relationship("Audit", back_populates="auditor", foreign_keys="Audit.auditor_id")
    nc_ofi_created = relationship("NCOFI", back_populates="raised_by_user", foreign_keys="NCOFI.raised_by")
    nc_ofi_assigned = relationship("NCOFI", back_populates="assigned_to_user", foreign_keys="NCOFI.assigned_to")
    cars_created = relationship("CorrectiveAction", back_populates="created_by_user", foreign_keys="CorrectiveAction.created_by")

    def set_password(self, password: str):
        """
        Hash and set user password

        Args:
            password: Plain text password
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """
        Verify password against hash

        Args:
            password: Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"

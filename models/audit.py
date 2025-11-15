"""
Audit Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    audit_number = Column(String(50), unique=True, nullable=False, index=True)
    audit_type = Column(String(50), nullable=False)  # Internal, External, Supplier, etc.
    standard = Column(String(50))  # ISO 9001, IATF 16949, VDA 6.3
    department = Column(String(100))
    auditor_id = Column(Integer, ForeignKey("users.id"))
    auditee_id = Column(Integer, ForeignKey("users.id"))
    audit_date = Column(Date, nullable=False)
    status = Column(String(50), default="Planned")  # Planned, InProgress, Completed, Closed
    scope = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    auditor = relationship("User", foreign_keys=[auditor_id])
    auditee = relationship("User", foreign_keys=[auditee_id])

    def __repr__(self):
        return f"<Audit {self.audit_number}>"

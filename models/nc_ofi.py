"""
NC/OFI (Non-Conformity / Opportunity for Improvement) Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class NCOFI(Base):
    __tablename__ = "nc_ofi"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=False, index=True)
    type = Column(String(10), nullable=False)  # NC or OFI
    category = Column(String(50))  # Major, Minor, Observation
    clause_no = Column(String(50), index=True)  # ISO clause reference
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # Critical, Major, Minor
    status = Column(String(20), default="Open", nullable=False)  # Open, InProgress, Verified, Closed
    assignee_id = Column(Integer, ForeignKey("users.id"), index=True)
    due_date = Column(Date)
    closure_date = Column(Date)
    evidence_path = Column(String(500))  # Path to evidence files/documents
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    audit = relationship("Audit", backref="findings")
    assignee = relationship("User", backref="assigned_findings")

    def __repr__(self):
        return f"<NCOFI {self.type}-{self.id}: {self.severity} - {self.status}>"

    @property
    def days_open(self):
        """Calculate number of days the finding has been open"""
        if self.closure_date:
            return (self.closure_date - self.created_at.date()).days
        return (datetime.utcnow().date() - self.created_at.date()).days

    @property
    def is_overdue(self):
        """Check if finding is overdue"""
        if self.status in ["Verified", "Closed"] or not self.due_date:
            return False
        return datetime.utcnow().date() > self.due_date

    @property
    def days_until_due(self):
        """Calculate days until due date (negative if overdue)"""
        if not self.due_date:
            return None
        return (self.due_date - datetime.utcnow().date()).days

"""
Non-Conformance and Observation for Improvement model.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class NC_OFI(Base):
    """Non-Conformance and Observation for Improvement model."""

    __tablename__ = 'nc_ofis'

    # Primary fields
    id = Column(Integer, primary_key=True, index=True)
    nc_number = Column(String(50), unique=True, nullable=False, index=True)
    audit_id = Column(Integer, ForeignKey('audits.id'), nullable=False, index=True)

    # Classification
    finding_type = Column(String(50), nullable=False)  # Major NC, Minor NC, OFI
    category = Column(String(100))  # Process, Documentation, Resource, etc.
    severity = Column(String(50))  # Critical, High, Medium, Low

    # Finding details
    clause_reference = Column(String(100))  # Standard clause reference
    requirement = Column(Text, nullable=False)  # What was expected
    observation = Column(Text, nullable=False)  # What was found
    evidence = Column(Text)  # Evidence/proof of the finding

    # Location and responsibility
    location = Column(String(200))
    department = Column(String(100))
    process_owner = Column(String(100))

    # Status tracking
    status = Column(String(50), default='Open')  # Open, CAR Initiated, In Progress, Closed, Verified
    priority = Column(String(50), default='Medium')  # Low, Medium, High, Critical

    # Closure details
    immediate_action = Column(Text)  # Quick fix applied
    target_closure_date = Column(DateTime)
    actual_closure_date = Column(DateTime)
    closure_notes = Column(Text)
    verified_by = Column(String(100))
    verified_date = Column(DateTime)

    # Flags
    is_repeat_finding = Column(Boolean, default=False)
    requires_car = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    raised_by = Column(String(100))

    # Relationships
    audit = relationship("Audit", back_populates="nc_ofis")
    corrective_actions = relationship("CorrectiveAction", back_populates="nc_ofi", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<NC_OFI(id={self.id}, number='{self.nc_number}', type='{self.finding_type}', status='{self.status}')>"

    def to_dict(self):
        """Convert NC/OFI to dictionary."""
        return {
            'id': self.id,
            'nc_number': self.nc_number,
            'audit_id': self.audit_id,
            'finding_type': self.finding_type,
            'category': self.category,
            'severity': self.severity,
            'clause_reference': self.clause_reference,
            'requirement': self.requirement,
            'observation': self.observation,
            'evidence': self.evidence,
            'location': self.location,
            'department': self.department,
            'process_owner': self.process_owner,
            'status': self.status,
            'priority': self.priority,
            'immediate_action': self.immediate_action,
            'target_closure_date': self.target_closure_date.isoformat() if self.target_closure_date else None,
            'actual_closure_date': self.actual_closure_date.isoformat() if self.actual_closure_date else None,
            'is_repeat_finding': self.is_repeat_finding,
            'requires_car': self.requires_car,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

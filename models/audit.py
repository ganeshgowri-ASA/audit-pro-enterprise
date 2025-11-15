"""
Audit model for managing audit records.
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Audit(Base):
    """Audit model representing an audit event."""

    __tablename__ = 'audits'

    # Primary fields
    id = Column(Integer, primary_key=True, index=True)
    audit_number = Column(String(50), unique=True, nullable=False, index=True)
    audit_type = Column(String(50), nullable=False)  # Internal, External, Supplier, etc.
    standard = Column(String(100), nullable=False)  # ISO 9001, IATF 16949, VDA 6.3

    # Entity information
    entity_name = Column(String(200), nullable=False)
    entity_location = Column(String(200))
    department = Column(String(100))

    # Audit scheduling
    planned_date = Column(Date, nullable=False)
    actual_date = Column(Date)
    duration_hours = Column(Float)

    # Audit team
    lead_auditor = Column(String(100), nullable=False)
    audit_team = Column(Text)  # JSON or comma-separated list
    auditee = Column(String(100))

    # Audit results
    status = Column(String(50), default='Planned')  # Planned, In Progress, Completed, Cancelled
    overall_score = Column(Float)
    compliance_percentage = Column(Float)

    # Findings summary
    total_findings = Column(Integer, default=0)
    major_nc_count = Column(Integer, default=0)
    minor_nc_count = Column(Integer, default=0)
    ofi_count = Column(Integer, default=0)

    # Documentation
    audit_plan = Column(Text)
    executive_summary = Column(Text)
    scope = Column(Text)
    observations = Column(Text)
    conclusions = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))

    # Relationships
    nc_ofis = relationship("NC_OFI", back_populates="audit", cascade="all, delete-orphan")
    reports = relationship("AuditReport", back_populates="audit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Audit(id={self.id}, number='{self.audit_number}', status='{self.status}')>"

    def to_dict(self):
        """Convert audit to dictionary."""
        return {
            'id': self.id,
            'audit_number': self.audit_number,
            'audit_type': self.audit_type,
            'standard': self.standard,
            'entity_name': self.entity_name,
            'entity_location': self.entity_location,
            'department': self.department,
            'planned_date': self.planned_date.isoformat() if self.planned_date else None,
            'actual_date': self.actual_date.isoformat() if self.actual_date else None,
            'duration_hours': self.duration_hours,
            'lead_auditor': self.lead_auditor,
            'audit_team': self.audit_team,
            'auditee': self.auditee,
            'status': self.status,
            'overall_score': self.overall_score,
            'compliance_percentage': self.compliance_percentage,
            'total_findings': self.total_findings,
            'major_nc_count': self.major_nc_count,
            'minor_nc_count': self.minor_nc_count,
            'ofi_count': self.ofi_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

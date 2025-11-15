"""
Audit Report model for managing generated reports.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class AuditReport(Base):
    """Audit Report model for tracking generated reports."""

    __tablename__ = 'audit_reports'

    # Primary fields
    id = Column(Integer, primary_key=True, index=True)
    report_number = Column(String(50), unique=True, nullable=False, index=True)
    audit_id = Column(Integer, ForeignKey('audits.id'), nullable=False, index=True)

    # Report metadata
    report_type = Column(String(50), nullable=False)
    # Types: Audit Report, NC Summary, CAR Status, Management Review, Executive Summary

    # Report content
    summary = Column(Text)
    executive_summary = Column(Text)
    findings_summary = Column(Text)
    recommendations = Column(Text)
    action_items = Column(Text)  # JSON array

    # PDF generation
    pdf_path = Column(String(500))
    pdf_generated = Column(DateTime)
    pdf_size_bytes = Column(Integer)

    # Report scope
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    scope = Column(Text)

    # Statistics included in report
    total_audits = Column(Integer)
    total_nc = Column(Integer)
    total_ofi = Column(Integer)
    total_cars = Column(Integer)
    completion_rate = Column(String(20))
    average_score = Column(String(20))

    # Distribution
    distributed_to = Column(Text)  # JSON array of recipients
    distribution_date = Column(DateTime)
    email_sent = Column(String(10), default='No')  # Yes/No

    # Metadata
    generated_at = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    audit = relationship("Audit", back_populates="reports")

    def __repr__(self):
        return f"<AuditReport(id={self.id}, number='{self.report_number}', type='{self.report_type}')>"

    def to_dict(self):
        """Convert report to dictionary."""
        return {
            'id': self.id,
            'report_number': self.report_number,
            'audit_id': self.audit_id,
            'report_type': self.report_type,
            'summary': self.summary,
            'executive_summary': self.executive_summary,
            'recommendations': self.recommendations,
            'pdf_path': self.pdf_path,
            'pdf_generated': self.pdf_generated.isoformat() if self.pdf_generated else None,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'generated_by': self.generated_by,
            'total_audits': self.total_audits,
            'total_nc': self.total_nc,
            'total_ofi': self.total_ofi,
            'completion_rate': self.completion_rate,
        }

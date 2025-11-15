"""
Audit Models
AuditPro Enterprise - Audit programs, types, schedules, and audits
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class AuditProgram(BaseModel):
    """
    Audit Program - Annual audit plan
    """
    __tablename__ = "audit_programs"

    # Program information
    year = Column(Integer, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    standard = Column(String(50))  # ISO 9001, IATF 16949, VDA 6.3, etc.

    # Status
    status = Column(String(50), default="Draft")  # Draft, Approved, Active, Completed

    # Relationships
    schedules = relationship("AuditSchedule", back_populates="program")

    def __repr__(self):
        return f"<AuditProgram(id={self.id}, year={self.year}, name={self.name})>"


class AuditType(BaseModel):
    """
    Audit Type - Classification of audits
    """
    __tablename__ = "audit_types"

    # Type information
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # Internal, External, Supplier, Product, Process, System

    # Relationships
    audits = relationship("Audit", back_populates="audit_type")

    def __repr__(self):
        return f"<AuditType(id={self.id}, code={self.code}, name={self.name})>"


class AuditSchedule(BaseModel):
    """
    Audit Schedule - Planned audits in the annual program
    """
    __tablename__ = "audit_schedules"

    # Schedule information
    program_id = Column(Integer, ForeignKey("audit_programs.id"), nullable=False)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    audit_type_id = Column(Integer, ForeignKey("audit_types.id"), nullable=False)

    # Planned dates
    planned_month = Column(Integer)  # 1-12
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)

    # Assignment
    planned_auditor_id = Column(Integer, ForeignKey("users.id"))

    # Status
    status = Column(String(50), default="Scheduled")  # Scheduled, Confirmed, Completed, Rescheduled, Cancelled

    # Relationships
    program = relationship("AuditProgram", back_populates="schedules")
    entity = relationship("Entity")
    audit_type = relationship("AuditType")
    planned_auditor = relationship("User")
    audits = relationship("Audit", back_populates="schedule")

    def __repr__(self):
        return f"<AuditSchedule(id={self.id}, entity_id={self.entity_id}, month={self.planned_month})>"


class Audit(BaseModel):
    """
    Audit - Actual audit execution
    """
    __tablename__ = "audits"

    # Audit identification
    audit_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)

    # Links
    schedule_id = Column(Integer, ForeignKey("audit_schedules.id"), nullable=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    audit_type_id = Column(Integer, ForeignKey("audit_types.id"), nullable=False)
    auditor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Audit details
    standard = Column(String(50))  # ISO 9001, IATF 16949, etc.
    scope = Column(Text)
    objectives = Column(Text)

    # Dates
    audit_date = Column(Date, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    # Participants
    auditee_names = Column(Text)  # Comma-separated or JSON

    # Results
    status = Column(String(50), default="Planned")  # Planned, In Progress, Completed, Cancelled
    overall_score = Column(Float)  # Percentage score
    conformance_level = Column(String(50))  # Conforming, Minor NC, Major NC, Critical

    # Summary
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    executive_summary = Column(Text)

    # Counts
    nc_count = Column(Integer, default=0)
    ofi_count = Column(Integer, default=0)

    # Report
    report_generated = Column(Boolean, default=False)
    report_path = Column(String(500))

    # Relationships
    schedule = relationship("AuditSchedule", back_populates="audits")
    entity = relationship("Entity", back_populates="audits")
    audit_type = relationship("AuditType", back_populates="audits")
    auditor = relationship("User", back_populates="audits_conducted", foreign_keys=[auditor_id])
    responses = relationship("AuditResponse", back_populates="audit")
    nc_ofis = relationship("NCOFI", back_populates="audit")

    def __repr__(self):
        return f"<Audit(id={self.id}, number={self.audit_number}, status={self.status})>"


class AuditReport(BaseModel):
    """
    Audit Report - Generated reports
    """
    __tablename__ = "audit_reports"

    # Report information
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=False)
    report_type = Column(String(50))  # Full Report, Summary, NC Report, etc.
    report_number = Column(String(50), unique=True)

    # File information
    file_path = Column(String(500))
    file_format = Column(String(20))  # PDF, XLSX, DOCX

    # Generation details
    generated_by = Column(Integer, ForeignKey("users.id"))
    generation_date = Column(DateTime)

    # Relationships
    audit = relationship("Audit")
    generator = relationship("User")

    def __repr__(self):
        return f"<AuditReport(id={self.id}, number={self.report_number}, type={self.report_type})>"

"""
Checklist Models
AuditPro Enterprise - Audit checklists and responses
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Checklist(BaseModel):
    """
    Checklist Template - Reusable audit checklist
    """
    __tablename__ = "checklists"

    # Checklist information
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    # Classification
    standard = Column(String(50))  # ISO 9001, IATF 16949, VDA 6.3, etc.
    category = Column(String(100))  # Process, Product, System, etc.
    version = Column(String(20), default="1.0")

    # Status
    is_active = Column(Boolean, default=True)

    # Relationships
    items = relationship("ChecklistItem", back_populates="checklist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Checklist(id={self.id}, code={self.code}, name={self.name})>"


class ChecklistItem(BaseModel):
    """
    Checklist Item - Individual question/requirement in checklist
    """
    __tablename__ = "checklist_items"

    # Item information
    checklist_id = Column(Integer, ForeignKey("checklists.id"), nullable=False)
    item_number = Column(String(20), nullable=False)  # e.g., "4.1.1", "P1.1"
    question = Column(Text, nullable=False)
    requirement = Column(Text)  # What is required for conformance

    # Classification
    clause_reference = Column(String(50))  # ISO clause reference
    process_area = Column(String(100))
    criticality = Column(String(20))  # Critical, Major, Minor

    # Scoring
    max_score = Column(Float, default=1.0)
    weight = Column(Float, default=1.0)

    # Order
    sequence = Column(Integer)

    # Relationships
    checklist = relationship("Checklist", back_populates="items")
    responses = relationship("AuditResponse", back_populates="checklist_item")

    def __repr__(self):
        return f"<ChecklistItem(id={self.id}, number={self.item_number}, question={self.question[:50]})>"


class AuditResponse(BaseModel):
    """
    Audit Response - Answer to checklist item during audit
    """
    __tablename__ = "audit_responses"

    # Links
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=False)
    checklist_item_id = Column(Integer, ForeignKey("checklist_items.id"), nullable=False)

    # Response
    conformance = Column(String(20))  # Conforming, NC, OFI, N/A
    score = Column(Float)  # Actual score achieved
    percentage = Column(Float)  # Percentage of max_score

    # Evidence and notes
    observations = Column(Text)
    evidence = Column(Text)  # File paths or references
    nc_ofi_raised = Column(Boolean, default=False)
    nc_ofi_id = Column(Integer, ForeignKey("nc_ofi.id"), nullable=True)

    # Audit trail
    assessed_by = Column(Integer, ForeignKey("users.id"))
    assessment_date = Column(String(50))

    # Relationships
    audit = relationship("Audit", back_populates="responses")
    checklist_item = relationship("ChecklistItem", back_populates="responses")
    assessor = relationship("User")
    nc_ofi = relationship("NCOFI")

    def __repr__(self):
        return f"<AuditResponse(id={self.id}, audit_id={self.audit_id}, conformance={self.conformance})>"

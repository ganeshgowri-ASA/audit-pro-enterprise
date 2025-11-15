"""
NC/OFI Model
AuditPro Enterprise - Non-Conformances and Opportunities for Improvement
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class NCOFI(BaseModel):
    """
    Non-Conformance / Opportunity for Improvement
    """
    __tablename__ = "nc_ofi"

    # Identification
    nc_number = Column(String(50), unique=True, nullable=False, index=True)
    finding_type = Column(String(20), nullable=False)  # NC, OFI

    # Classification (for NC)
    severity = Column(String(20))  # Critical, Major, Minor, Observation

    # Source
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    source = Column(String(50))  # Audit, Customer Complaint, Internal Review, etc.

    # Finding details
    description = Column(Text, nullable=False)
    requirement = Column(Text)  # What was expected
    evidence = Column(Text)  # Evidence of non-conformance
    clause_reference = Column(String(100))  # ISO clause or standard reference

    # Impact
    actual_impact = Column(Text)
    potential_impact = Column(Text)
    risk_level = Column(String(20))  # High, Medium, Low

    # Assignment
    raised_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    raised_date = Column(Date, nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    assigned_date = Column(Date)
    department = Column(String(100))

    # Target dates
    target_containment_date = Column(Date)  # For immediate action
    target_closure_date = Column(Date)  # For final resolution
    actual_closure_date = Column(Date)

    # Status tracking
    status = Column(String(50), default="Open")  # Open, In Progress, Closed, Verified, Rejected
    containment_status = Column(String(50))  # Not Started, In Progress, Completed
    root_cause_status = Column(String(50))  # Not Started, In Progress, Completed
    corrective_action_status = Column(String(50))  # Not Started, In Progress, Completed

    # Immediate containment
    immediate_action = Column(Text)
    immediate_action_by = Column(Integer, ForeignKey("users.id"))
    immediate_action_date = Column(Date)

    # Response
    root_cause = Column(Text)
    corrective_action_plan = Column(Text)
    preventive_action_plan = Column(Text)

    # Verification
    verification_required = Column(Boolean, default=True)
    verified_by = Column(Integer, ForeignKey("users.id"))
    verification_date = Column(Date)
    verification_notes = Column(Text)
    effectiveness_verified = Column(Boolean, default=False)

    # Metrics
    days_open = Column(Integer)  # Auto-calculated
    is_overdue = Column(Boolean, default=False)

    # Links to CAR
    car_required = Column(Boolean, default=False)
    car_id = Column(Integer, ForeignKey("corrective_actions.id"), nullable=True)

    # Relationships
    audit = relationship("Audit", back_populates="nc_ofis")
    entity = relationship("Entity")
    raised_by_user = relationship("User", foreign_keys=[raised_by], back_populates="nc_ofi_created")
    assigned_to_user = relationship("User", foreign_keys=[assigned_to], back_populates="nc_ofi_assigned")
    immediate_action_user = relationship("User", foreign_keys=[immediate_action_by])
    verifier = relationship("User", foreign_keys=[verified_by])
    car = relationship("CorrectiveAction", foreign_keys=[car_id], back_populates="nc_ofi")

    def calculate_days_open(self):
        """Calculate number of days the NC/OFI has been open"""
        from datetime import date
        if self.actual_closure_date:
            delta = self.actual_closure_date - self.raised_date
        else:
            delta = date.today() - self.raised_date
        self.days_open = delta.days
        return self.days_open

    def check_overdue(self):
        """Check if NC/OFI is overdue"""
        from datetime import date
        if self.target_closure_date and not self.actual_closure_date:
            self.is_overdue = date.today() > self.target_closure_date
        else:
            self.is_overdue = False
        return self.is_overdue

    def __repr__(self):
        return f"<NCOFI(id={self.id}, number={self.nc_number}, type={self.finding_type}, status={self.status})>"

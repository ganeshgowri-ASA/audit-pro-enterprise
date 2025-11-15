"""
Corrective Action (CAR/8D) Model
AuditPro Enterprise - 8D Methodology for problem solving
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class CorrectiveAction(BaseModel):
    """
    Corrective Action Report (CAR) using 8D methodology
    """
    __tablename__ = "corrective_actions"

    # Identification
    car_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)

    # Source
    nc_ofi_id = Column(Integer, ForeignKey("nc_ofi.id"), nullable=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    source = Column(String(50))  # NC, Customer Complaint, Internal Issue, etc.

    # Ownership
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_date = Column(Date, nullable=False)
    team_leader = Column(Integer, ForeignKey("users.id"))
    team_members = Column(Text)  # JSON or comma-separated user IDs

    # 8D Steps Status
    status = Column(String(50), default="Initiated")  # Initiated, In Progress, Closed, Verified

    # D1: Team Formation
    d1_team_formed = Column(Boolean, default=False)
    d1_team_description = Column(Text)
    d1_completed_date = Column(Date)

    # D2: Problem Description
    d2_problem_description = Column(Text)
    d2_is_vs_is_not = Column(Text)  # 5W2H analysis
    d2_completed_date = Column(Date)

    # D3: Interim Containment Actions
    d3_containment_action = Column(Text)
    d3_containment_responsible = Column(Integer, ForeignKey("users.id"))
    d3_containment_date = Column(Date)
    d3_containment_verified = Column(Boolean, default=False)
    d3_completed_date = Column(Date)

    # D4: Root Cause Analysis
    d4_root_cause_method = Column(String(50))  # 5 Why, Fishbone, FTA, etc.
    d4_potential_causes = Column(Text)
    d4_root_cause = Column(Text)
    d4_verification_method = Column(Text)
    d4_verification_results = Column(Text)
    d4_completed_date = Column(Date)

    # D5: Corrective Actions
    d5_corrective_actions = Column(Text)  # JSON array of actions
    d5_responsible = Column(Integer, ForeignKey("users.id"))
    d5_target_date = Column(Date)
    d5_completed_date = Column(Date)

    # D6: Implementation and Validation
    d6_implementation_plan = Column(Text)
    d6_implementation_status = Column(String(50))
    d6_validation_method = Column(Text)
    d6_validation_results = Column(Text)
    d6_validation_date = Column(Date)
    d6_completed_date = Column(Date)

    # D7: Preventive Actions
    d7_preventive_actions = Column(Text)
    d7_systems_updated = Column(Text)  # SOPs, Work Instructions updated
    d7_training_conducted = Column(Boolean, default=False)
    d7_training_records = Column(Text)
    d7_completed_date = Column(Date)

    # D8: Team Recognition and Closure
    d8_lessons_learned = Column(Text)
    d8_best_practices = Column(Text)
    d8_team_recognition = Column(Text)
    d8_closure_date = Column(Date)
    d8_completed_date = Column(Date)

    # Effectiveness Verification
    verification_required = Column(Boolean, default=True)
    verification_plan = Column(Text)
    verification_date = Column(Date)
    verified_by = Column(Integer, ForeignKey("users.id"))
    effectiveness_confirmed = Column(Boolean, default=False)
    verification_notes = Column(Text)

    # Attachments and evidence
    attachments = Column(Text)  # JSON array of file paths

    # Metrics
    days_to_close = Column(Integer)
    is_overdue = Column(Boolean, default=False)

    # Relationships
    nc_ofi = relationship("NCOFI", foreign_keys="NCOFI.car_id", back_populates="car")
    entity = relationship("Entity")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="cars_created")
    team_leader_user = relationship("User", foreign_keys=[team_leader])
    d3_responsible_user = relationship("User", foreign_keys=[d3_containment_responsible])
    d5_responsible_user = relationship("User", foreign_keys=[d5_responsible])
    verifier_user = relationship("User", foreign_keys=[verified_by])

    def calculate_completion_percentage(self):
        """Calculate overall completion percentage based on 8D steps"""
        steps_completed = sum([
            self.d1_team_formed,
            bool(self.d2_problem_description),
            bool(self.d3_containment_action),
            bool(self.d4_root_cause),
            bool(self.d5_corrective_actions),
            bool(self.d6_implementation_status == "Completed"),
            bool(self.d7_preventive_actions),
            bool(self.d8_closure_date)
        ])
        return (steps_completed / 8) * 100

    def get_current_step(self):
        """Determine the current 8D step"""
        if not self.d1_team_formed:
            return "D1: Team Formation"
        elif not self.d2_problem_description:
            return "D2: Problem Description"
        elif not self.d3_containment_action:
            return "D3: Interim Containment"
        elif not self.d4_root_cause:
            return "D4: Root Cause Analysis"
        elif not self.d5_corrective_actions:
            return "D5: Corrective Actions"
        elif self.d6_implementation_status != "Completed":
            return "D6: Implementation & Validation"
        elif not self.d7_preventive_actions:
            return "D7: Preventive Actions"
        elif not self.d8_closure_date:
            return "D8: Closure"
        else:
            return "Completed"

    def __repr__(self):
        return f"<CorrectiveAction(id={self.id}, number={self.car_number}, status={self.status})>"

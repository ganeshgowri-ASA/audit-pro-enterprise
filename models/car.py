"""
Corrective Action Request (CAR) model with 8D methodology support.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class CorrectiveAction(Base):
    """Corrective Action Request with 8D methodology fields."""

    __tablename__ = 'corrective_actions'

    # Primary fields
    id = Column(Integer, primary_key=True, index=True)
    car_number = Column(String(50), unique=True, nullable=False, index=True)
    nc_ofi_id = Column(Integer, ForeignKey('nc_ofis.id'), nullable=False, index=True)

    # CAR methodology
    method = Column(String(50), default='8D')  # 8D, 5Why, Fishbone, PDCA

    # Basic CAR fields
    root_cause = Column(Text)
    immediate_action = Column(Text)
    permanent_action = Column(Text)
    action_plan = Column(Text)

    # Responsibility and timeline
    responsible_person = Column(String(100))
    due_date = Column(Date)
    completion_date = Column(Date)

    # Verification
    effectiveness_verified = Column(Boolean, default=False)
    verification_method = Column(Text)
    verification_date = Column(Date)
    verified_by = Column(String(100))
    verification_notes = Column(Text)

    # Status
    status = Column(String(50), default='Draft')
    # Draft, Submitted, Approved, In Progress, Implemented, Verified, Closed

    # === 8D METHODOLOGY FIELDS ===

    # D1: Team Formation
    d1_team = Column(Text)  # JSON array of team members with roles
    d1_team_leader = Column(String(100))
    d1_team_members = Column(Text)  # Comma-separated or JSON
    d1_completion_date = Column(Date)
    d1_notes = Column(Text)

    # D2: Problem Description (5W2H)
    d2_problem_description = Column(Text)
    d2_what = Column(Text)  # What is the problem?
    d2_when = Column(Text)  # When did it occur?
    d2_where = Column(Text)  # Where did it occur?
    d2_who = Column(Text)  # Who discovered it?
    d2_why = Column(Text)  # Why is it a problem?
    d2_how = Column(Text)  # How was it detected?
    d2_how_many = Column(Text)  # How many are affected?
    d2_completion_date = Column(Date)
    d2_notes = Column(Text)

    # D3: Containment Actions
    d3_containment = Column(Text)
    d3_immediate_actions = Column(Text)
    d3_containment_verified = Column(Boolean, default=False)
    d3_effectiveness = Column(Text)
    d3_completion_date = Column(Date)
    d3_notes = Column(Text)

    # D4: Root Cause Analysis
    d4_root_cause = Column(Text)
    d4_analysis_method = Column(String(50))  # 5-Why, Fishbone, etc.
    d4_why1 = Column(Text)  # For 5-Why analysis
    d4_why2 = Column(Text)
    d4_why3 = Column(Text)
    d4_why4 = Column(Text)
    d4_why5 = Column(Text)
    d4_fishbone_data = Column(Text)  # JSON for fishbone diagram
    d4_root_cause_verified = Column(Boolean, default=False)
    d4_completion_date = Column(Date)
    d4_notes = Column(Text)

    # D5: Permanent Corrective Actions
    d5_corrective_actions = Column(Text)
    d5_action_items = Column(Text)  # JSON array of action items
    d5_why_selected = Column(Text)  # Why these actions were selected
    d5_completion_date = Column(Date)
    d5_notes = Column(Text)

    # D6: Implementation
    d6_implementation = Column(Text)
    d6_implementation_plan = Column(Text)
    d6_resources_required = Column(Text)
    d6_training_required = Column(Text)
    d6_timeline = Column(Text)
    d6_milestones = Column(Text)  # JSON array
    d6_completion_date = Column(Date)
    d6_notes = Column(Text)

    # D7: Prevention Measures
    d7_prevention = Column(Text)
    d7_process_changes = Column(Text)
    d7_system_improvements = Column(Text)
    d7_documentation_updates = Column(Text)
    d7_training_plan = Column(Text)
    d7_completion_date = Column(Date)
    d7_notes = Column(Text)

    # D8: Team Recognition
    d8_recognition = Column(Text)
    d8_team_contributions = Column(Text)
    d8_lessons_learned = Column(Text)
    d8_best_practices = Column(Text)
    d8_recognition_method = Column(Text)
    d8_completion_date = Column(Date)
    d8_notes = Column(Text)

    # === ADDITIONAL TRACKING ===

    # Attachments and evidence
    attachments = Column(Text)  # JSON array of file paths

    # Approval workflow
    submitted_by = Column(String(100))
    submitted_date = Column(Date)
    approved_by = Column(String(100))
    approved_date = Column(Date)
    approval_notes = Column(Text)

    # Notifications
    notification_sent = Column(Boolean, default=False)
    reminder_sent = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))

    # Relationships
    nc_ofi = relationship("NC_OFI", back_populates="corrective_actions")

    def __repr__(self):
        return f"<CorrectiveAction(id={self.id}, number='{self.car_number}', method='{self.method}', status='{self.status}')>"

    def get_8d_progress(self):
        """Calculate 8D completion progress (0-100%)."""
        disciplines_completed = 0
        total_disciplines = 8

        if self.d1_completion_date:
            disciplines_completed += 1
        if self.d2_completion_date:
            disciplines_completed += 1
        if self.d3_completion_date:
            disciplines_completed += 1
        if self.d4_completion_date:
            disciplines_completed += 1
        if self.d5_completion_date:
            disciplines_completed += 1
        if self.d6_completion_date:
            disciplines_completed += 1
        if self.d7_completion_date:
            disciplines_completed += 1
        if self.d8_completion_date:
            disciplines_completed += 1

        return (disciplines_completed / total_disciplines) * 100

    def to_dict(self):
        """Convert CAR to dictionary."""
        return {
            'id': self.id,
            'car_number': self.car_number,
            'nc_ofi_id': self.nc_ofi_id,
            'method': self.method,
            'root_cause': self.root_cause,
            'immediate_action': self.immediate_action,
            'permanent_action': self.permanent_action,
            'responsible_person': self.responsible_person,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'status': self.status,
            'effectiveness_verified': self.effectiveness_verified,
            '8d_progress': self.get_8d_progress(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

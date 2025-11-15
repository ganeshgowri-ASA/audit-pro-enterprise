"""
Tests for CAR (Corrective Action Request) and 8D Methodology

Test coverage:
- CAR creation and lifecycle
- 8D workflow progression (D1-D8)
- Root cause analysis (5-Why, Fishbone)
- Effectiveness verification
- Status transitions
"""

import pytest
from datetime import date, timedelta
from database import get_db, init_db, reset_db, Base
from models.audit import Audit
from models.nc_ofi import NC_OFI
from models.car import CorrectiveAction


@pytest.fixture(scope='function')
def db():
    """Create a fresh database for each test."""
    reset_db()
    db = get_db()
    yield db
    db.close()


@pytest.fixture
def sample_audit(db):
    """Create a sample audit for testing."""
    audit = Audit(
        audit_number="AUD-TEST-001",
        audit_type="Internal",
        standard="ISO 9001:2015",
        entity_name="Test Entity",
        planned_date=date.today(),
        actual_date=date.today(),
        lead_auditor="Test Auditor",
        status="Completed",
        overall_score=85.5,
        compliance_percentage=90.0,
        created_by="Test User"
    )
    db.add(audit)
    db.commit()
    return audit


@pytest.fixture
def sample_nc(db, sample_audit):
    """Create a sample NC for testing."""
    nc = NC_OFI(
        nc_number="NC-TEST-001",
        audit_id=sample_audit.id,
        finding_type="Major NC",
        category="Process",
        severity="High",
        requirement="Process shall be documented",
        observation="Process documentation not found",
        status="Open",
        requires_car=True,
        raised_by="Test Auditor"
    )
    db.add(nc)
    db.commit()
    return nc


class TestCARCreation:
    """Test CAR creation and basic functionality."""

    def test_create_car(self, db, sample_nc):
        """Test creating a new CAR."""
        car = CorrectiveAction(
            car_number="CAR-TEST-001",
            nc_ofi_id=sample_nc.id,
            method="8D",
            responsible_person="John Doe",
            due_date=date.today() + timedelta(days=30),
            status="Draft",
            created_by="Test User"
        )

        db.add(car)
        db.commit()

        assert car.id is not None
        assert car.car_number == "CAR-TEST-001"
        assert car.method == "8D"
        assert car.status == "Draft"

    def test_car_nc_relationship(self, db, sample_nc):
        """Test CAR-NC relationship."""
        car = CorrectiveAction(
            car_number="CAR-TEST-002",
            nc_ofi_id=sample_nc.id,
            method="8D",
            responsible_person="Jane Smith",
            due_date=date.today() + timedelta(days=30),
            status="Draft"
        )

        db.add(car)
        db.commit()

        # Test relationship
        assert car.nc_ofi.nc_number == sample_nc.nc_number
        assert sample_nc.corrective_actions[0].car_number == car.car_number

    def test_car_methods(self, db, sample_nc):
        """Test different CAR methods."""
        methods = ["8D", "5Why", "Fishbone", "PDCA"]

        for i, method in enumerate(methods):
            car = CorrectiveAction(
                car_number=f"CAR-TEST-{i:03d}",
                nc_ofi_id=sample_nc.id,
                method=method,
                responsible_person="Test Person",
                due_date=date.today() + timedelta(days=30),
                status="Draft"
            )
            db.add(car)

        db.commit()

        cars = db.query(CorrectiveAction).all()
        assert len(cars) == 4
        assert set([car.method for car in cars]) == set(methods)


class Test8DWorkflow:
    """Test 8D methodology workflow."""

    @pytest.fixture
    def car_8d(self, db, sample_nc):
        """Create a CAR with 8D method for testing."""
        car = CorrectiveAction(
            car_number="CAR-8D-001",
            nc_ofi_id=sample_nc.id,
            method="8D",
            responsible_person="8D Team Lead",
            due_date=date.today() + timedelta(days=60),
            status="Approved",
            created_by="Test User"
        )
        db.add(car)
        db.commit()
        return car

    def test_d1_team_formation(self, db, car_8d):
        """Test D1: Team Formation."""
        car_8d.d1_team_leader = "John Smith"
        car_8d.d1_team_members = "Jane Doe - Quality Engineer\nBob Wilson - Production Lead"
        car_8d.d1_completion_date = date.today()
        car_8d.d1_notes = "Cross-functional team formed"

        db.commit()

        assert car_8d.d1_team_leader == "John Smith"
        assert "Jane Doe" in car_8d.d1_team_members
        assert car_8d.d1_completion_date is not None

    def test_d2_problem_description(self, db, car_8d):
        """Test D2: Problem Description (5W2H)."""
        car_8d.d2_what = "Defective parts found in production"
        car_8d.d2_when = "Discovered on 2024-01-15"
        car_8d.d2_where = "Production Line 1"
        car_8d.d2_who = "Quality Inspector"
        car_8d.d2_why = "Potential customer impact"
        car_8d.d2_how = "Through routine inspection"
        car_8d.d2_how_many = "50 units affected"
        car_8d.d2_completion_date = date.today()

        db.commit()

        assert car_8d.d2_what is not None
        assert car_8d.d2_when is not None
        assert car_8d.d2_where is not None

    def test_d3_containment(self, db, car_8d):
        """Test D3: Containment Actions."""
        car_8d.d3_immediate_actions = "Quarantine all affected products"
        car_8d.d3_containment_verified = True
        car_8d.d3_effectiveness = "100% containment achieved"
        car_8d.d3_completion_date = date.today()

        db.commit()

        assert car_8d.d3_immediate_actions is not None
        assert car_8d.d3_containment_verified is True

    def test_d4_root_cause_5why(self, db, car_8d):
        """Test D4: Root Cause Analysis using 5-Why."""
        car_8d.d4_analysis_method = "5-Why"
        car_8d.d4_why1 = "Why did defects occur? - Incorrect machine settings"
        car_8d.d4_why2 = "Why incorrect settings? - Operator error"
        car_8d.d4_why3 = "Why operator error? - Inadequate training"
        car_8d.d4_why4 = "Why inadequate training? - Training program outdated"
        car_8d.d4_why5 = "Why training outdated? - No regular review process [ROOT CAUSE]"
        car_8d.d4_root_cause = car_8d.d4_why5
        car_8d.d4_root_cause_verified = True
        car_8d.d4_completion_date = date.today()

        db.commit()

        assert car_8d.d4_analysis_method == "5-Why"
        assert car_8d.d4_why5 is not None
        assert car_8d.d4_root_cause_verified is True

    def test_d4_root_cause_fishbone(self, db, car_8d):
        """Test D4: Root Cause Analysis using Fishbone."""
        import json

        fishbone_data = {
            "man": "Operator inexperience",
            "method": "Process not followed",
            "machine": "Equipment malfunction",
            "material": "Defective raw material",
            "measurement": "Incorrect calibration",
            "environment": "Temperature variation"
        }

        car_8d.d4_analysis_method = "Fishbone"
        car_8d.d4_fishbone_data = json.dumps(fishbone_data)
        car_8d.d4_root_cause = "Equipment malfunction due to lack of preventive maintenance"
        car_8d.d4_root_cause_verified = True
        car_8d.d4_completion_date = date.today()

        db.commit()

        assert car_8d.d4_analysis_method == "Fishbone"
        assert car_8d.d4_fishbone_data is not None

        loaded_data = json.loads(car_8d.d4_fishbone_data)
        assert loaded_data["machine"] == "Equipment malfunction"

    def test_d5_corrective_actions(self, db, car_8d):
        """Test D5: Permanent Corrective Actions."""
        car_8d.d5_corrective_actions = "1. Update training program\n2. Implement preventive maintenance\n3. Add verification step"
        car_8d.d5_why_selected = "These actions address the root cause directly"
        car_8d.d5_completion_date = date.today()

        db.commit()

        assert car_8d.d5_corrective_actions is not None
        assert "training" in car_8d.d5_corrective_actions.lower()

    def test_d6_implementation(self, db, car_8d):
        """Test D6: Implementation."""
        car_8d.d6_implementation_plan = "Phase 1: Documentation\nPhase 2: Training\nPhase 3: Verification"
        car_8d.d6_resources_required = "Budget: $10,000, Personnel: 3"
        car_8d.d6_training_required = "8-hour training for all operators"
        car_8d.d6_timeline = "4 weeks"
        car_8d.d6_completion_date = date.today()

        db.commit()

        assert car_8d.d6_implementation_plan is not None
        assert car_8d.d6_resources_required is not None

    def test_d7_prevention(self, db, car_8d):
        """Test D7: Prevention Measures."""
        car_8d.d7_process_changes = "Updated standard operating procedures"
        car_8d.d7_system_improvements = "Implemented automated monitoring"
        car_8d.d7_documentation_updates = "Revised training materials"
        car_8d.d7_training_plan = "Quarterly refresher training"
        car_8d.d7_completion_date = date.today()

        db.commit()

        assert car_8d.d7_process_changes is not None
        assert car_8d.d7_system_improvements is not None

    def test_d8_recognition(self, db, car_8d):
        """Test D8: Team Recognition."""
        car_8d.d8_team_contributions = "Team showed excellent collaboration"
        car_8d.d8_lessons_learned = "Importance of preventive maintenance"
        car_8d.d8_best_practices = "8D methodology proven effective"
        car_8d.d8_recognition_method = "Team celebration lunch"
        car_8d.d8_completion_date = date.today()

        db.commit()

        assert car_8d.d8_team_contributions is not None
        assert car_8d.d8_lessons_learned is not None

    def test_8d_progress_calculation(self, db, car_8d):
        """Test 8D progress calculation."""
        # Initially 0%
        assert car_8d.get_8d_progress() == 0.0

        # Complete D1
        car_8d.d1_completion_date = date.today()
        assert car_8d.get_8d_progress() == 12.5  # 1/8 * 100

        # Complete D2
        car_8d.d2_completion_date = date.today()
        assert car_8d.get_8d_progress() == 25.0  # 2/8 * 100

        # Complete all disciplines
        car_8d.d3_completion_date = date.today()
        car_8d.d4_completion_date = date.today()
        car_8d.d5_completion_date = date.today()
        car_8d.d6_completion_date = date.today()
        car_8d.d7_completion_date = date.today()
        car_8d.d8_completion_date = date.today()

        assert car_8d.get_8d_progress() == 100.0

    def test_complete_8d_workflow(self, db, car_8d):
        """Test complete 8D workflow from start to finish."""
        # D1: Team
        car_8d.d1_team_leader = "Team Lead"
        car_8d.d1_team_members = "Member 1, Member 2"
        car_8d.d1_completion_date = date.today()

        # D2: Problem
        car_8d.d2_what = "Problem description"
        car_8d.d2_completion_date = date.today() + timedelta(days=1)

        # D3: Containment
        car_8d.d3_immediate_actions = "Containment actions"
        car_8d.d3_containment_verified = True
        car_8d.d3_completion_date = date.today() + timedelta(days=2)

        # D4: Root Cause
        car_8d.d4_root_cause = "Root cause identified"
        car_8d.d4_root_cause_verified = True
        car_8d.d4_completion_date = date.today() + timedelta(days=5)

        # D5: Actions
        car_8d.d5_corrective_actions = "Corrective actions"
        car_8d.d5_completion_date = date.today() + timedelta(days=7)

        # D6: Implementation
        car_8d.d6_implementation_plan = "Implementation plan"
        car_8d.d6_completion_date = date.today() + timedelta(days=21)

        # D7: Prevention
        car_8d.d7_prevention = "Prevention measures"
        car_8d.d7_completion_date = date.today() + timedelta(days=28)

        # D8: Recognition
        car_8d.d8_recognition = "Team recognition"
        car_8d.d8_completion_date = date.today() + timedelta(days=30)

        car_8d.status = "Implemented"
        car_8d.completion_date = date.today() + timedelta(days=30)

        db.commit()

        # Verify complete workflow
        assert car_8d.get_8d_progress() == 100.0
        assert car_8d.status == "Implemented"
        assert car_8d.completion_date is not None


class TestEffectivenessVerification:
    """Test effectiveness verification functionality."""

    @pytest.fixture
    def completed_car(self, db, sample_nc):
        """Create a completed CAR for verification testing."""
        car = CorrectiveAction(
            car_number="CAR-VERIFY-001",
            nc_ofi_id=sample_nc.id,
            method="8D",
            responsible_person="Test Person",
            due_date=date.today(),
            completion_date=date.today() - timedelta(days=30),
            status="Implemented",
            root_cause="Root cause identified",
            permanent_action="Permanent action taken",
            created_by="Test User"
        )

        # Complete all 8D disciplines
        for i in range(1, 9):
            setattr(car, f'd{i}_completion_date', date.today() - timedelta(days=30-i))

        db.add(car)
        db.commit()
        return car

    def test_effectiveness_verification(self, db, completed_car):
        """Test CAR effectiveness verification."""
        completed_car.effectiveness_verified = True
        completed_car.verification_method = "Follow-up audit"
        completed_car.verification_date = date.today()
        completed_car.verified_by = "Quality Manager"
        completed_car.verification_notes = "Actions verified effective"
        completed_car.status = "Verified"

        db.commit()

        assert completed_car.effectiveness_verified is True
        assert completed_car.verification_method is not None
        assert completed_car.status == "Verified"

    def test_verification_workflow(self, db, completed_car):
        """Test verification workflow steps."""
        # Initial state
        assert completed_car.status == "Implemented"
        assert completed_car.effectiveness_verified is False

        # Perform verification
        completed_car.effectiveness_verified = True
        completed_car.verified_by = "Verifier"
        completed_car.verification_date = date.today()
        completed_car.status = "Verified"

        db.commit()

        # Verify final state
        verified_car = db.query(CorrectiveAction).filter_by(
            car_number="CAR-VERIFY-001"
        ).first()

        assert verified_car.effectiveness_verified is True
        assert verified_car.status == "Verified"
        assert verified_car.verified_by == "Verifier"


class TestCARStatusTransitions:
    """Test CAR status transitions."""

    @pytest.fixture
    def car(self, db, sample_nc):
        """Create a CAR for status transition testing."""
        car = CorrectiveAction(
            car_number="CAR-STATUS-001",
            nc_ofi_id=sample_nc.id,
            method="8D",
            responsible_person="Test Person",
            due_date=date.today() + timedelta(days=30),
            status="Draft",
            created_by="Test User"
        )
        db.add(car)
        db.commit()
        return car

    def test_status_progression(self, db, car):
        """Test CAR status progression."""
        # Draft -> Submitted
        car.status = "Submitted"
        car.submitted_by = "Submitter"
        car.submitted_date = date.today()
        db.commit()
        assert car.status == "Submitted"

        # Submitted -> Approved
        car.status = "Approved"
        car.approved_by = "Approver"
        car.approved_date = date.today()
        db.commit()
        assert car.status == "Approved"

        # Approved -> In Progress
        car.status = "In Progress"
        db.commit()
        assert car.status == "In Progress"

        # In Progress -> Implemented
        car.status = "Implemented"
        car.completion_date = date.today()
        db.commit()
        assert car.status == "Implemented"

        # Implemented -> Verified
        car.status = "Verified"
        car.effectiveness_verified = True
        car.verification_date = date.today()
        db.commit()
        assert car.status == "Verified"

    def test_to_dict(self, db, car):
        """Test CAR to_dict method."""
        car_dict = car.to_dict()

        assert car_dict['car_number'] == "CAR-STATUS-001"
        assert car_dict['method'] == "8D"
        assert car_dict['status'] == "Draft"
        assert '8d_progress' in car_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

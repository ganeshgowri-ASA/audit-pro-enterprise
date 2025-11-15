"""
Tests for NC/OFI tracking system
"""
import pytest
from datetime import datetime, timedelta
from models.nc_ofi import NCOFI
from models.nc_ofi_history import NCOFIHistory
from models.user import User
from models.audit import Audit


class TestNCCreation:
    """Tests for NC/OFI creation"""

    def test_nc_creation(self, db_session, sample_audit, sample_user):
        """Test creating a new NC finding"""
        # Create NC
        nc = NCOFI(
            audit_id=sample_audit.id,
            type="NC",
            category="Major",
            severity="Critical",
            clause_no="7.5.3",
            description="Document control non-conformity",
            status="Open",
            assignee_id=sample_user.id,
            due_date=datetime.now().date() + timedelta(days=30)
        )

        db_session.add(nc)
        db_session.commit()

        # Verify NC was created
        assert nc.id is not None
        assert nc.type == "NC"
        assert nc.severity == "Critical"
        assert nc.status == "Open"
        assert nc.assignee_id == sample_user.id
        assert nc.audit_id == sample_audit.id

    def test_ofi_creation(self, db_session, sample_audit, sample_user):
        """Test creating a new OFI finding"""
        # Create OFI
        ofi = NCOFI(
            audit_id=sample_audit.id,
            type="OFI",
            category="Observation",
            severity="Minor",
            clause_no="9.1.2",
            description="Opportunity to implement automated reporting",
            status="Open",
            assignee_id=sample_user.id,
            due_date=datetime.now().date() + timedelta(days=60)
        )

        db_session.add(ofi)
        db_session.commit()

        # Verify OFI was created
        assert ofi.id is not None
        assert ofi.type == "OFI"
        assert ofi.severity == "Minor"
        assert ofi.status == "Open"

    def test_nc_creation_with_all_fields(self, db_session, sample_audit, sample_user):
        """Test creating NC with all optional fields"""
        nc = NCOFI(
            audit_id=sample_audit.id,
            type="NC",
            category="Minor",
            severity="Major",
            clause_no="8.6",
            description="Product release verification not performed",
            status="Open",
            assignee_id=sample_user.id,
            due_date=datetime.now().date() + timedelta(days=30),
            evidence_path="/evidence/photos/nc_001.jpg"
        )

        db_session.add(nc)
        db_session.commit()

        # Verify all fields
        assert nc.id is not None
        assert nc.evidence_path == "/evidence/photos/nc_001.jpg"
        assert nc.created_at is not None

    def test_nc_relationships(self, db_session, sample_nc):
        """Test NC relationships with audit and user"""
        # Verify relationships work
        assert sample_nc.audit is not None
        assert sample_nc.audit.audit_number == "TEST-001"
        assert sample_nc.assignee is not None
        assert sample_nc.assignee.full_name == "Test User"


class TestStatusWorkflow:
    """Tests for status workflow transitions"""

    def test_status_workflow(self, db_session, sample_nc):
        """Test complete status workflow: Open → InProgress → Verified → Closed"""

        # Initial status should be Open
        assert sample_nc.status == "Open"

        # Transition to InProgress
        sample_nc.status = "InProgress"
        history1 = NCOFIHistory(
            nc_ofi_id=sample_nc.id,
            old_status="Open",
            new_status="InProgress",
            comment="Root cause analysis initiated"
        )
        db_session.add(history1)
        db_session.commit()

        assert sample_nc.status == "InProgress"

        # Transition to Verified
        sample_nc.status = "Verified"
        history2 = NCOFIHistory(
            nc_ofi_id=sample_nc.id,
            old_status="InProgress",
            new_status="Verified",
            comment="Corrective action implemented and verified"
        )
        db_session.add(history2)
        db_session.commit()

        assert sample_nc.status == "Verified"

        # Transition to Closed
        sample_nc.status = "Closed"
        sample_nc.closure_date = datetime.now().date()
        history3 = NCOFIHistory(
            nc_ofi_id=sample_nc.id,
            old_status="Verified",
            new_status="Closed",
            comment="Finding closed by management"
        )
        db_session.add(history3)
        db_session.commit()

        assert sample_nc.status == "Closed"
        assert sample_nc.closure_date is not None

    def test_status_history_tracking(self, db_session, sample_nc):
        """Test that status changes are tracked in history"""

        # Create history record
        history = NCOFIHistory(
            nc_ofi_id=sample_nc.id,
            old_status="Open",
            new_status="InProgress",
            comment="Test status change"
        )
        db_session.add(history)
        db_session.commit()

        # Query history
        histories = db_session.query(NCOFIHistory).filter(
            NCOFIHistory.nc_ofi_id == sample_nc.id
        ).all()

        assert len(histories) >= 1
        assert histories[0].old_status == "Open"
        assert histories[0].new_status == "InProgress"
        assert histories[0].comment == "Test status change"

    def test_closure_date_set_on_close(self, db_session, sample_nc):
        """Test that closure_date is set when status changes to Closed"""

        # Initially no closure date
        assert sample_nc.closure_date is None

        # Close the finding
        closure_date = datetime.now().date()
        sample_nc.status = "Closed"
        sample_nc.closure_date = closure_date
        db_session.commit()

        assert sample_nc.status == "Closed"
        assert sample_nc.closure_date == closure_date

    def test_status_workflow_history_chain(self, db_session, sample_nc):
        """Test complete workflow with history chain"""

        # Create complete workflow history
        statuses = ["Open", "InProgress", "Verified", "Closed"]

        for i in range(len(statuses) - 1):
            old_status = statuses[i]
            new_status = statuses[i + 1]

            sample_nc.status = new_status
            history = NCOFIHistory(
                nc_ofi_id=sample_nc.id,
                old_status=old_status,
                new_status=new_status,
                comment=f"Transition {old_status} to {new_status}"
            )
            db_session.add(history)
            db_session.commit()

        # Verify history chain
        histories = db_session.query(NCOFIHistory).filter(
            NCOFIHistory.nc_ofi_id == sample_nc.id
        ).order_by(NCOFIHistory.changed_at).all()

        assert len(histories) == 3  # 3 transitions for 4 statuses
        assert histories[0].new_status == "InProgress"
        assert histories[1].new_status == "Verified"
        assert histories[2].new_status == "Closed"


class TestAgingCalculation:
    """Tests for aging and overdue calculations"""

    def test_aging_calculation(self, db_session, sample_nc):
        """Test days_open calculation"""

        # For a newly created finding, days_open should be 0 or 1
        assert sample_nc.days_open >= 0

        # Create finding with specific creation date
        old_nc = NCOFI(
            audit_id=sample_nc.audit_id,
            type="NC",
            category="Major",
            severity="Major",
            clause_no="8.5.1",
            description="Old finding",
            status="Open",
            assignee_id=sample_nc.assignee_id,
            due_date=datetime.now().date() + timedelta(days=30),
            created_at=datetime.now() - timedelta(days=45)
        )
        db_session.add(old_nc)
        db_session.commit()

        # Should be approximately 45 days old
        assert old_nc.days_open >= 44
        assert old_nc.days_open <= 46

    def test_aging_with_closure_date(self, db_session, sample_nc):
        """Test days_open calculation with closure_date"""

        # Set creation and closure dates
        sample_nc.created_at = datetime.now() - timedelta(days=30)
        sample_nc.closure_date = (datetime.now() - timedelta(days=10)).date()
        db_session.commit()

        # Days open should be 20 (30 - 10)
        assert sample_nc.days_open >= 19
        assert sample_nc.days_open <= 21

    def test_overdue_detection(self, db_session, sample_audit, sample_user):
        """Test is_overdue property"""

        # Create overdue finding (due yesterday)
        overdue_nc = NCOFI(
            audit_id=sample_audit.id,
            type="NC",
            category="Major",
            severity="Critical",
            clause_no="8.5.1",
            description="Overdue finding",
            status="Open",
            assignee_id=sample_user.id,
            due_date=datetime.now().date() - timedelta(days=1)
        )
        db_session.add(overdue_nc)
        db_session.commit()

        assert overdue_nc.is_overdue is True

    def test_not_overdue(self, db_session, sample_nc):
        """Test finding that is not overdue"""

        # sample_nc has due date 30 days in future
        assert sample_nc.is_overdue is False

    def test_days_until_due(self, db_session, sample_nc):
        """Test days_until_due calculation"""

        # sample_nc is due in 30 days
        days_until_due = sample_nc.days_until_due

        assert days_until_due >= 29
        assert days_until_due <= 31

    def test_overdue_not_applicable_when_closed(self, db_session, sample_nc):
        """Test that closed findings are not marked as overdue"""

        # Set past due date
        sample_nc.due_date = datetime.now().date() - timedelta(days=10)
        sample_nc.status = "Closed"
        sample_nc.closure_date = datetime.now().date()
        db_session.commit()

        # Should not be overdue since it's closed
        assert sample_nc.is_overdue is False

    def test_aging_for_multiple_findings(self, db_session, sample_audit, sample_user):
        """Test aging calculation for multiple findings with different ages"""

        findings = []
        ages = [5, 15, 30, 60, 90]

        for age in ages:
            nc = NCOFI(
                audit_id=sample_audit.id,
                type="NC",
                category="Major",
                severity="Major",
                clause_no="8.5.1",
                description=f"Finding aged {age} days",
                status="Open",
                assignee_id=sample_user.id,
                due_date=datetime.now().date() + timedelta(days=30),
                created_at=datetime.now() - timedelta(days=age)
            )
            db_session.add(nc)
            findings.append(nc)

        db_session.commit()

        # Verify aging for each finding
        for i, finding in enumerate(findings):
            expected_age = ages[i]
            # Allow 1 day tolerance
            assert finding.days_open >= expected_age - 1
            assert finding.days_open <= expected_age + 1


class TestQueryFiltering:
    """Tests for querying and filtering findings"""

    def test_filter_by_status(self, db_session, sample_nc, sample_ofi):
        """Test filtering findings by status"""

        # Both should be Open
        open_findings = db_session.query(NCOFI).filter(NCOFI.status == "Open").all()
        assert len(open_findings) >= 2

        # Change one to Closed
        sample_nc.status = "Closed"
        db_session.commit()

        open_findings = db_session.query(NCOFI).filter(NCOFI.status == "Open").all()
        closed_findings = db_session.query(NCOFI).filter(NCOFI.status == "Closed").all()

        assert len(closed_findings) >= 1
        assert sample_nc in closed_findings

    def test_filter_by_type(self, db_session, sample_nc, sample_ofi):
        """Test filtering by NC vs OFI"""

        ncs = db_session.query(NCOFI).filter(NCOFI.type == "NC").all()
        ofis = db_session.query(NCOFI).filter(NCOFI.type == "OFI").all()

        assert sample_nc in ncs
        assert sample_ofi in ofis
        assert sample_nc not in ofis
        assert sample_ofi not in ncs

    def test_filter_by_severity(self, db_session, sample_audit, sample_user):
        """Test filtering by severity"""

        # Create findings with different severities
        critical_nc = NCOFI(
            audit_id=sample_audit.id,
            type="NC",
            category="Major",
            severity="Critical",
            clause_no="8.5.1",
            description="Critical finding",
            status="Open",
            assignee_id=sample_user.id,
            due_date=datetime.now().date() + timedelta(days=7)
        )
        db_session.add(critical_nc)
        db_session.commit()

        critical_findings = db_session.query(NCOFI).filter(
            NCOFI.severity == "Critical"
        ).all()

        assert critical_nc in critical_findings

    def test_filter_by_assignee(self, db_session, sample_nc, sample_user):
        """Test filtering by assignee"""

        user_findings = db_session.query(NCOFI).filter(
            NCOFI.assignee_id == sample_user.id
        ).all()

        assert sample_nc in user_findings

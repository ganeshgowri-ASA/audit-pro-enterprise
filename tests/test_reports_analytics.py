"""
Tests for Reports & Analytics

Test coverage:
- PDF report generation
- KPI calculation
- Trend analysis
- Data export functionality
- Analytics calculations
"""

import pytest
from datetime import date, datetime, timedelta
from database import get_db, init_db, reset_db
from models.audit import Audit
from models.nc_ofi import NC_OFI
from models.car import CorrectiveAction
from models.reports import AuditReport
from utils.pdf_generator import (
    generate_audit_pdf,
    generate_nc_summary_pdf,
    generate_car_status_pdf
)
import os


@pytest.fixture(scope='function')
def db():
    """Create a fresh database for each test."""
    reset_db()
    db = get_db()
    yield db
    db.close()


@pytest.fixture
def sample_audits(db):
    """Create sample audits for testing."""
    audits = []

    for i in range(12):
        days_ago = i * 30
        audit = Audit(
            audit_number=f"AUD-2024-{i+1:03d}",
            audit_type="Internal",
            standard="ISO 9001:2015",
            entity_name=f"Entity {i % 3}",
            entity_location="Test Location",
            department="Quality",
            planned_date=date.today() - timedelta(days=days_ago),
            actual_date=date.today() - timedelta(days=days_ago - 2),
            duration_hours=8.0,
            lead_auditor=f"Auditor {i % 2}",
            status="Completed",
            overall_score=70.0 + (i * 2),  # Scores from 70 to 92
            compliance_percentage=75.0 + (i * 2),
            total_findings=10 - i % 5,
            major_nc_count=i % 3,
            minor_nc_count=i % 4,
            ofi_count=i % 5,
            created_by="Test User"
        )
        db.add(audit)
        audits.append(audit)

    db.commit()
    return audits


@pytest.fixture
def sample_nc_ofis(db, sample_audits):
    """Create sample NC/OFI for testing."""
    nc_ofis = []

    for i, audit in enumerate(sample_audits[:5]):
        for j in range(3):
            nc = NC_OFI(
                nc_number=f"NC-2024-{i:02d}{j:02d}",
                audit_id=audit.id,
                finding_type=["Major NC", "Minor NC", "OFI"][j % 3],
                category=["Process", "Documentation", "Resource"][j % 3],
                severity=["Critical", "High", "Medium", "Low"][j % 4],
                requirement="Test requirement",
                observation="Test observation",
                status=["Open", "In Progress", "Closed"][j % 3],
                raised_by=audit.lead_auditor
            )
            db.add(nc)
            nc_ofis.append(nc)

    db.commit()
    return nc_ofis


@pytest.fixture
def sample_cars(db, sample_nc_ofis):
    """Create sample CARs for testing."""
    cars = []

    for i, nc in enumerate(sample_nc_ofis[:8]):
        car = CorrectiveAction(
            car_number=f"CAR-2024-{i+1:03d}",
            nc_ofi_id=nc.id,
            method="8D",
            responsible_person="Test Person",
            due_date=date.today() + timedelta(days=30),
            status=["Draft", "Approved", "In Progress", "Implemented", "Verified"][i % 5],
            created_by="Test User"
        )

        # Complete 8D for verified CARs
        if car.status == "Verified":
            for d in range(1, 9):
                setattr(car, f'd{d}_completion_date', date.today() - timedelta(days=30-d))
            car.effectiveness_verified = True

        db.add(car)
        cars.append(car)

    db.commit()
    return cars


class TestPDFGeneration:
    """Test PDF report generation."""

    def test_generate_audit_pdf(self, db, sample_audits, sample_nc_ofis):
        """Test audit report PDF generation."""
        audit = sample_audits[0]
        nc_ofis = [nc for nc in sample_nc_ofis if nc.audit_id == audit.id]

        output_path = "data/sample_pdfs/test_audit_report.pdf"

        # Generate PDF
        result_path = generate_audit_pdf(audit, nc_ofis, output_path)

        assert os.path.exists(result_path)
        assert os.path.getsize(result_path) > 0

        # Cleanup
        if os.path.exists(result_path):
            os.remove(result_path)

    def test_generate_nc_summary_pdf(self, db, sample_nc_ofis):
        """Test NC/OFI summary PDF generation."""
        date_from = date.today() - timedelta(days=365)
        date_to = date.today()
        output_path = "data/sample_pdfs/test_nc_summary.pdf"

        # Generate PDF
        result_path = generate_nc_summary_pdf(
            sample_nc_ofis,
            date_from,
            date_to,
            output_path
        )

        assert os.path.exists(result_path)
        assert os.path.getsize(result_path) > 0

        # Cleanup
        if os.path.exists(result_path):
            os.remove(result_path)

    def test_generate_car_status_pdf(self, db, sample_cars):
        """Test CAR status report PDF generation."""
        output_path = "data/sample_pdfs/test_car_status.pdf"

        # Generate PDF
        result_path = generate_car_status_pdf(sample_cars, output_path)

        assert os.path.exists(result_path)
        assert os.path.getsize(result_path) > 0

        # Cleanup
        if os.path.exists(result_path):
            os.remove(result_path)

    def test_pdf_with_empty_data(self, db):
        """Test PDF generation with empty data."""
        output_path = "data/sample_pdfs/test_empty.pdf"

        # Should handle empty NC list gracefully
        result_path = generate_nc_summary_pdf(
            [],
            date.today() - timedelta(days=30),
            date.today(),
            output_path
        )

        assert os.path.exists(result_path)

        # Cleanup
        if os.path.exists(result_path):
            os.remove(result_path)


class TestKPICalculation:
    """Test KPI calculation functions."""

    def calculate_kpis(self, db, date_from, date_to):
        """Helper function to calculate KPIs."""
        # Total audits
        total_audits = db.query(Audit).filter(
            Audit.planned_date >= date_from,
            Audit.planned_date <= date_to
        ).count()

        # Completed audits
        completed_audits = db.query(Audit).filter(
            Audit.planned_date >= date_from,
            Audit.planned_date <= date_to,
            Audit.status == 'Completed'
        ).count()

        # Completion rate
        completion_rate = (completed_audits / total_audits * 100) if total_audits > 0 else 0

        # Average audit score
        audits = db.query(Audit).filter(
            Audit.planned_date >= date_from,
            Audit.planned_date <= date_to,
            Audit.overall_score.isnot(None)
        ).all()
        avg_score = sum([a.overall_score for a in audits]) / len(audits) if audits else 0

        # Open NC count
        open_nc = db.query(NC_OFI).filter(
            NC_OFI.status.in_(['Open', 'CAR Initiated', 'In Progress'])
        ).count()

        # Total NC/OFI
        total_nc = db.query(NC_OFI).filter(NC_OFI.finding_type.in_(['Major NC', 'Minor NC'])).count()

        # NC closure rate
        closed_nc = db.query(NC_OFI).filter(
            NC_OFI.status == 'Closed',
            NC_OFI.finding_type.in_(['Major NC', 'Minor NC'])
        ).count()
        nc_closure_rate = (closed_nc / total_nc * 100) if total_nc > 0 else 0

        return {
            'total_audits': total_audits,
            'completed_audits': completed_audits,
            'completion_rate': completion_rate,
            'avg_score': avg_score,
            'open_nc': open_nc,
            'total_nc': total_nc,
            'nc_closure_rate': nc_closure_rate
        }

    def test_kpi_total_audits(self, db, sample_audits):
        """Test total audits KPI calculation."""
        date_from = date.today() - timedelta(days=365)
        date_to = date.today()

        kpis = self.calculate_kpis(db, date_from, date_to)

        assert kpis['total_audits'] == len(sample_audits)

    def test_kpi_completion_rate(self, db, sample_audits):
        """Test completion rate KPI calculation."""
        date_from = date.today() - timedelta(days=365)
        date_to = date.today()

        kpis = self.calculate_kpis(db, date_from, date_to)

        # All sample audits are completed
        assert kpis['completion_rate'] == 100.0

    def test_kpi_average_score(self, db, sample_audits):
        """Test average audit score KPI calculation."""
        date_from = date.today() - timedelta(days=365)
        date_to = date.today()

        kpis = self.calculate_kpis(db, date_from, date_to)

        # Calculate expected average
        scores = [audit.overall_score for audit in sample_audits]
        expected_avg = sum(scores) / len(scores)

        assert abs(kpis['avg_score'] - expected_avg) < 0.01

    def test_kpi_open_nc(self, db, sample_nc_ofis):
        """Test open NC count KPI calculation."""
        date_from = date.today() - timedelta(days=365)
        date_to = date.today()

        kpis = self.calculate_kpis(db, date_from, date_to)

        # Count expected open NCs
        expected_open = len([nc for nc in sample_nc_ofis if nc.status in ['Open', 'In Progress']])

        assert kpis['open_nc'] == expected_open

    def test_kpi_nc_closure_rate(self, db, sample_nc_ofis):
        """Test NC closure rate KPI calculation."""
        date_from = date.today() - timedelta(days=365)
        date_to = date.today()

        kpis = self.calculate_kpis(db, date_from, date_to)

        # Verify closure rate calculation
        assert 0 <= kpis['nc_closure_rate'] <= 100

    def test_kpi_with_no_data(self, db):
        """Test KPI calculation with no data."""
        date_from = date.today() - timedelta(days=30)
        date_to = date.today()

        kpis = self.calculate_kpis(db, date_from, date_to)

        assert kpis['total_audits'] == 0
        assert kpis['completion_rate'] == 0
        assert kpis['avg_score'] == 0


class TestTrendAnalysis:
    """Test trend analysis functionality."""

    def test_audit_score_trend(self, db, sample_audits):
        """Test audit score trend calculation."""
        # Get audits ordered by date
        audits = db.query(Audit).filter(
            Audit.overall_score.isnot(None)
        ).order_by(Audit.actual_date).all()

        assert len(audits) == len(sample_audits)

        # Verify trend (scores should increase over time in our sample data)
        scores = [a.overall_score for a in audits]

        # Calculate trend (simple linear)
        first_half_avg = sum(scores[:6]) / 6
        second_half_avg = sum(scores[6:]) / 6

        assert second_half_avg > first_half_avg  # Improving trend

    def test_monthly_audit_count(self, db, sample_audits):
        """Test monthly audit count trend."""
        # Group audits by month
        from collections import defaultdict

        monthly_counts = defaultdict(int)

        for audit in sample_audits:
            month_key = audit.planned_date.strftime('%Y-%m')
            monthly_counts[month_key] += 1

        assert len(monthly_counts) > 0
        assert all(count > 0 for count in monthly_counts.values())

    def test_nc_severity_distribution(self, db, sample_nc_ofis):
        """Test NC severity distribution analysis."""
        from collections import Counter

        severity_counts = Counter([nc.severity for nc in sample_nc_ofis if nc.severity])

        # Verify we have different severity levels
        assert len(severity_counts) > 0

        # Total should match
        assert sum(severity_counts.values()) <= len(sample_nc_ofis)

    def test_repeat_findings_analysis(self, db, sample_nc_ofis):
        """Test repeat findings analysis."""
        # Mark some NCs as repeat findings
        for i, nc in enumerate(sample_nc_ofis[:3]):
            nc.is_repeat_finding = True

        db.commit()

        # Query repeat findings
        repeat_nc = db.query(NC_OFI).filter(NC_OFI.is_repeat_finding == True).all()

        assert len(repeat_nc) == 3

    def test_auditor_performance(self, db, sample_audits):
        """Test auditor performance analysis."""
        from collections import defaultdict

        auditor_data = defaultdict(lambda: {'audits': 0, 'scores': []})

        for audit in sample_audits:
            auditor = audit.lead_auditor
            auditor_data[auditor]['audits'] += 1
            if audit.overall_score:
                auditor_data[auditor]['scores'].append(audit.overall_score)

        # Calculate averages
        auditor_avg_scores = {
            auditor: sum(data['scores']) / len(data['scores']) if data['scores'] else 0
            for auditor, data in auditor_data.items()
        }

        # Verify we have auditor data
        assert len(auditor_avg_scores) > 0
        assert all(score >= 0 for score in auditor_avg_scores.values())


class TestAuditReportModel:
    """Test AuditReport model functionality."""

    def test_create_audit_report(self, db, sample_audits):
        """Test creating an audit report record."""
        audit = sample_audits[0]

        report = AuditReport(
            report_number="RPT-2024-001",
            audit_id=audit.id,
            report_type="Audit Report",
            summary="Test report summary",
            executive_summary="Test executive summary",
            recommendations="Test recommendations",
            pdf_path="data/sample_pdfs/test_report.pdf",
            generated_at=datetime.utcnow(),
            generated_by="Test User",
            total_audits=1,
            total_nc=5,
            total_ofi=3,
            completion_rate="100%",
            average_score="85.5"
        )

        db.add(report)
        db.commit()

        assert report.id is not None
        assert report.report_number == "RPT-2024-001"

    def test_report_audit_relationship(self, db, sample_audits):
        """Test report-audit relationship."""
        audit = sample_audits[0]

        report = AuditReport(
            report_number="RPT-2024-002",
            audit_id=audit.id,
            report_type="Executive Summary",
            summary="Test summary",
            generated_by="Test User"
        )

        db.add(report)
        db.commit()

        # Test relationship
        assert report.audit.audit_number == audit.audit_number
        assert len(audit.reports) > 0

    def test_report_types(self, db, sample_audits):
        """Test different report types."""
        audit = sample_audits[0]
        report_types = [
            "Audit Report",
            "NC Summary",
            "CAR Status",
            "Management Review",
            "Executive Summary"
        ]

        for i, report_type in enumerate(report_types):
            report = AuditReport(
                report_number=f"RPT-2024-{i+10:03d}",
                audit_id=audit.id,
                report_type=report_type,
                summary=f"Test {report_type}",
                generated_by="Test User"
            )
            db.add(report)

        db.commit()

        reports = db.query(AuditReport).all()
        report_type_set = set([r.report_type for r in reports])

        assert len(report_type_set) == len(report_types)

    def test_report_to_dict(self, db, sample_audits):
        """Test report to_dict method."""
        audit = sample_audits[0]

        report = AuditReport(
            report_number="RPT-2024-099",
            audit_id=audit.id,
            report_type="Test Report",
            summary="Test summary",
            generated_by="Test User",
            total_audits=10,
            total_nc=5,
            completion_rate="90%"
        )

        db.add(report)
        db.commit()

        report_dict = report.to_dict()

        assert report_dict['report_number'] == "RPT-2024-099"
        assert report_dict['report_type'] == "Test Report"
        assert report_dict['total_audits'] == 10
        assert 'generated_at' in report_dict


class TestDataExport:
    """Test data export functionality."""

    def test_export_audits_to_dict(self, db, sample_audits):
        """Test exporting audits to dictionary format."""
        audits_data = [audit.to_dict() for audit in sample_audits]

        assert len(audits_data) == len(sample_audits)
        assert all('audit_number' in data for data in audits_data)
        assert all('overall_score' in data for data in audits_data)

    def test_export_nc_ofis_to_dict(self, db, sample_nc_ofis):
        """Test exporting NC/OFI to dictionary format."""
        nc_data = [nc.to_dict() for nc in sample_nc_ofis]

        assert len(nc_data) == len(sample_nc_ofis)
        assert all('nc_number' in data for data in nc_data)
        assert all('finding_type' in data for data in nc_data)

    def test_export_cars_to_dict(self, db, sample_cars):
        """Test exporting CARs to dictionary format."""
        car_data = [car.to_dict() for car in sample_cars]

        assert len(car_data) == len(sample_cars)
        assert all('car_number' in data for data in car_data)
        assert all('8d_progress' in data for data in car_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Sample Data Generator for Audit Pro Enterprise

Generates realistic sample data for:
- Audits (12 months historical data)
- NC/OFI findings
- CARs with 8D methodology (8 total: 5 completed, 3 in-progress)
- Audit Reports with pre-generated PDFs
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, init_db
from models.audit import Audit
from models.nc_ofi import NC_OFI
from models.car import CorrectiveAction
from models.reports import AuditReport
from datetime import datetime, date, timedelta
from faker import Faker
import random

fake = Faker()


def generate_audits(db, count=24):
    """Generate sample audits over 12 months."""
    print(f"Generating {count} sample audits...")

    audit_types = ["Internal", "External", "Supplier", "Process", "Product"]
    standards = ["ISO 9001:2015", "IATF 16949:2016", "VDA 6.3"]
    entities = ["Manufacturing Plant A", "Quality Lab", "Engineering Center", "Supply Chain Dept", "Production Line 1"]
    departments = ["Quality", "Production", "Engineering", "Logistics", "Maintenance"]
    auditors = ["John Smith", "Sarah Johnson", "Mike Williams", "Emily Brown", "David Lee"]
    statuses = ["Completed", "Completed", "Completed", "In Progress", "Planned"]

    audits = []

    for i in range(count):
        # Distribute audits over 12 months
        days_ago = random.randint(0, 365)
        planned_date = date.today() - timedelta(days=days_ago)
        actual_date = planned_date + timedelta(days=random.randint(0, 7)) if days_ago > 7 else None

        status = random.choice(statuses)
        if status == "Planned":
            actual_date = None

        # Generate audit scores between 65-95
        overall_score = random.uniform(65, 95) if status == "Completed" else None
        compliance_percentage = random.uniform(70, 98) if status == "Completed" else None

        # Generate findings
        major_nc = random.randint(0, 3) if status == "Completed" else 0
        minor_nc = random.randint(0, 8) if status == "Completed" else 0
        ofi = random.randint(0, 12) if status == "Completed" else 0
        total_findings = major_nc + minor_nc + ofi

        audit = Audit(
            audit_number=f"AUD-{planned_date.strftime('%Y%m')}-{i+1:03d}",
            audit_type=random.choice(audit_types),
            standard=random.choice(standards),
            entity_name=random.choice(entities),
            entity_location=f"{fake.city()}, {fake.state()}",
            department=random.choice(departments),
            planned_date=planned_date,
            actual_date=actual_date,
            duration_hours=random.uniform(4, 16) if actual_date else None,
            lead_auditor=random.choice(auditors),
            audit_team=", ".join(random.sample(auditors, k=random.randint(2, 4))),
            auditee=fake.name(),
            status=status,
            overall_score=overall_score,
            compliance_percentage=compliance_percentage,
            total_findings=total_findings,
            major_nc_count=major_nc,
            minor_nc_count=minor_nc,
            ofi_count=ofi,
            audit_plan=f"Audit plan for {random.choice(entities)}",
            executive_summary=f"Audit completed with {total_findings} findings. Overall compliance is {'satisfactory' if compliance_percentage and compliance_percentage > 80 else 'needs improvement'}." if status == "Completed" else None,
            scope=f"Process audit covering {random.choice(departments)} operations",
            observations="Various observations noted during audit execution." if status == "Completed" else None,
            conclusions=f"System effectiveness is {'good' if overall_score and overall_score > 80 else 'acceptable'}." if status == "Completed" else None,
            created_by=random.choice(auditors),
            created_at=datetime.now() - timedelta(days=days_ago)
        )

        db.add(audit)
        audits.append(audit)

    db.commit()
    print(f"✅ Created {count} audits")
    return audits


def generate_nc_ofi(db, audits):
    """Generate NC/OFI findings for audits."""
    print("Generating NC/OFI findings...")

    finding_types = ["Major NC", "Minor NC", "OFI"]
    categories = ["Process", "Documentation", "Resource", "Equipment", "Training", "Material Handling"]
    severities = ["Critical", "High", "Medium", "Low"]
    statuses = ["Open", "CAR Initiated", "In Progress", "Closed", "Verified"]
    priorities = ["Critical", "High", "Medium", "Low"]

    nc_ofis = []
    nc_count = 0

    for audit in audits:
        if audit.status != "Completed":
            continue

        # Generate findings based on audit counts
        for _ in range(audit.major_nc_count):
            nc_count += 1
            nc = create_nc_ofi(db, audit, "Major NC", nc_count, categories, severities, statuses, priorities)
            nc_ofis.append(nc)

        for _ in range(audit.minor_nc_count):
            nc_count += 1
            nc = create_nc_ofi(db, audit, "Minor NC", nc_count, categories, severities, statuses, priorities)
            nc_ofis.append(nc)

        for _ in range(audit.ofi_count):
            nc_count += 1
            nc = create_nc_ofi(db, audit, "OFI", nc_count, categories, severities, statuses, priorities)
            nc_ofis.append(nc)

    db.commit()
    print(f"✅ Created {len(nc_ofis)} NC/OFI findings")
    return nc_ofis


def create_nc_ofi(db, audit, finding_type, nc_count, categories, severities, statuses, priorities):
    """Create a single NC/OFI record."""
    severity = "Critical" if finding_type == "Major NC" else random.choice(severities)
    priority = "High" if finding_type == "Major NC" else random.choice(priorities)

    # Determine status - older findings more likely to be closed
    days_since_audit = (date.today() - audit.actual_date).days
    if days_since_audit > 90:
        status = random.choice(["Closed", "Verified", "Verified"])
    elif days_since_audit > 30:
        status = random.choice(["In Progress", "CAR Initiated", "Closed"])
    else:
        status = random.choice(["Open", "CAR Initiated", "In Progress"])

    nc = NC_OFI(
        nc_number=f"NC-{audit.actual_date.strftime('%Y%m')}-{nc_count:04d}",
        audit_id=audit.id,
        finding_type=finding_type,
        category=random.choice(categories),
        severity=severity,
        clause_reference=f"{random.randint(4, 10)}.{random.randint(1, 5)}.{random.randint(1, 3)}",
        requirement=fake.sentence(nb_words=12),
        observation=fake.paragraph(nb_sentences=3),
        evidence=fake.sentence(nb_words=10),
        location=audit.entity_location,
        department=audit.department,
        process_owner=fake.name(),
        status=status,
        priority=priority,
        immediate_action=fake.sentence(nb_words=15) if status != "Open" else None,
        target_closure_date=audit.actual_date + timedelta(days=random.randint(30, 90)),
        actual_closure_date=audit.actual_date + timedelta(days=random.randint(30, 90)) if status in ["Closed", "Verified"] else None,
        closure_notes=fake.paragraph(nb_sentences=2) if status in ["Closed", "Verified"] else None,
        verified_by=fake.name() if status == "Verified" else None,
        verified_date=datetime.now() - timedelta(days=random.randint(0, 30)) if status == "Verified" else None,
        is_repeat_finding=random.choice([True, False]) if random.random() < 0.1 else False,
        requires_car=finding_type in ["Major NC", "Minor NC"] and random.random() < 0.6,
        raised_by=audit.lead_auditor,
        created_at=datetime.now() - timedelta(days=(date.today() - audit.actual_date).days)
    )

    db.add(nc)
    return nc


def generate_cars(db, nc_ofis):
    """Generate CARs with 8D methodology (5 completed, 3 in-progress)."""
    print("Generating CARs with 8D methodology...")

    # Filter NC/OFI that require CAR
    nc_requiring_car = [nc for nc in nc_ofis if nc.requires_car][:8]

    if len(nc_requiring_car) < 8:
        print(f"⚠️ Only {len(nc_requiring_car)} NC/OFI require CAR, generating {len(nc_requiring_car)} CARs")

    responsible_persons = ["John Smith", "Sarah Johnson", "Mike Williams", "Emily Brown", "David Lee"]
    cars = []

    for i, nc in enumerate(nc_requiring_car):
        # First 5 are completed, last 3 are in-progress
        is_completed = i < 5

        car_number = f"CAR-{nc.created_at.strftime('%Y%m%d')}-{i+1:03d}"
        responsible = random.choice(responsible_persons)

        due_date = nc.target_closure_date or (date.today() + timedelta(days=30))

        if is_completed:
            status = "Verified"
            completion_date = nc.actual_closure_date or (date.today() - timedelta(days=random.randint(1, 30)))
        else:
            status = random.choice(["Submitted", "Approved", "In Progress"])
            completion_date = None

        car = CorrectiveAction(
            car_number=car_number,
            nc_ofi_id=nc.id,
            method="8D",
            root_cause=fake.paragraph(nb_sentences=2) if is_completed else None,
            immediate_action=fake.sentence(nb_words=15),
            permanent_action=fake.paragraph(nb_sentences=2) if is_completed else None,
            action_plan=fake.paragraph(nb_sentences=3),
            responsible_person=responsible,
            due_date=due_date,
            completion_date=completion_date,
            effectiveness_verified=is_completed,
            verification_method="Follow-up audit and process monitoring" if is_completed else None,
            verification_date=completion_date,
            verified_by=fake.name() if is_completed else None,
            verification_notes="Verified effective through observation and data analysis" if is_completed else None,
            status=status,
            created_by=nc.raised_by,
            created_at=nc.created_at + timedelta(days=2)
        )

        # Populate 8D fields
        populate_8d_fields(car, is_completed, responsible, responsible_persons)

        db.add(car)
        cars.append(car)

    db.commit()
    print(f"✅ Created {len(cars)} CARs (5 completed, {len(cars)-5} in-progress)")
    return cars


def populate_8d_fields(car, is_completed, responsible, team_members):
    """Populate 8D methodology fields for a CAR."""

    # D1: Team Formation
    car.d1_team_leader = responsible
    car.d1_team_members = "\n".join([f"{name} - {random.choice(['Quality Engineer', 'Production Lead', 'Process Owner', 'Technician'])}" for name in random.sample(team_members, k=3)])
    car.d1_completion_date = car.created_at.date() + timedelta(days=1) if is_completed else None
    car.d1_notes = "Cross-functional team formed with relevant expertise"

    if is_completed or random.random() < 0.5:
        # D2: Problem Description
        car.d2_what = fake.sentence(nb_words=12)
        car.d2_when = f"First observed on {fake.date_between(start_date='-90d', end_date='today')}"
        car.d2_where = fake.sentence(nb_words=8)
        car.d2_who = fake.name()
        car.d2_why = fake.sentence(nb_words=10)
        car.d2_how = "Through routine inspection and quality checks"
        car.d2_how_many = f"Approximately {random.randint(5, 50)} units affected"
        car.d2_completion_date = car.d1_completion_date + timedelta(days=2) if car.d1_completion_date else None
        car.d2_notes = "Problem clearly defined using 5W2H method"

    if is_completed or random.random() < 0.4:
        # D3: Containment
        car.d3_immediate_actions = "1. Quarantine affected products\n2. Increase inspection frequency\n3. Notify relevant stakeholders"
        car.d3_containment_verified = True
        car.d3_effectiveness = "Containment verified effective - no further issues detected"
        car.d3_completion_date = car.d2_completion_date + timedelta(days=1) if car.d2_completion_date else None
        car.d3_notes = "Containment actions implemented successfully"

    if is_completed or random.random() < 0.3:
        # D4: Root Cause Analysis
        car.d4_analysis_method = "5-Why"
        car.d4_why1 = fake.sentence(nb_words=10)
        car.d4_why2 = fake.sentence(nb_words=10)
        car.d4_why3 = fake.sentence(nb_words=10)
        car.d4_why4 = fake.sentence(nb_words=10)
        car.d4_why5 = fake.sentence(nb_words=12) + " [ROOT CAUSE]"
        car.d4_root_cause = car.d4_why5
        car.d4_root_cause_verified = is_completed
        car.d4_completion_date = car.d3_completion_date + timedelta(days=3) if car.d3_completion_date else None
        car.d4_notes = "Root cause identified and verified through analysis"

    if is_completed or random.random() < 0.2:
        # D5: Corrective Actions
        car.d5_corrective_actions = "1. Update process documentation\n2. Implement poka-yoke device\n3. Revise training program\n4. Modify work instructions"
        car.d5_why_selected = "These actions address the root cause and prevent recurrence"
        car.d5_completion_date = car.d4_completion_date + timedelta(days=2) if car.d4_completion_date else None
        car.d5_notes = "Actions selected based on root cause analysis"

    if is_completed:
        # D6: Implementation
        car.d6_implementation_plan = "Phase 1: Documentation update\nPhase 2: Equipment installation\nPhase 3: Training rollout\nPhase 4: Process verification"
        car.d6_resources_required = "Budget: $5,000\nPersonnel: 3 engineers\nEquipment: Inspection tools"
        car.d6_training_required = "4-hour training session for all operators"
        car.d6_timeline = "4 weeks total implementation"
        car.d6_completion_date = car.d5_completion_date + timedelta(days=14) if car.d5_completion_date else None
        car.d6_notes = "Implementation completed on schedule"

        # D7: Prevention
        car.d7_process_changes = "Updated process flow to include additional verification step"
        car.d7_system_improvements = "Implemented automated monitoring system"
        car.d7_documentation_updates = "Updated SOPs, work instructions, and training materials"
        car.d7_training_plan = "Quarterly refresher training for all relevant personnel"
        car.d7_completion_date = car.d6_completion_date + timedelta(days=7) if car.d6_completion_date else None
        car.d7_notes = "Systemic changes implemented to prevent recurrence"

        # D8: Recognition
        car.d8_team_contributions = "Team demonstrated excellent collaboration and problem-solving skills"
        car.d8_lessons_learned = "Importance of early detection and cross-functional teamwork"
        car.d8_best_practices = "8D methodology proven effective for complex problem solving"
        car.d8_recognition_method = "Team lunch and recognition certificate"
        car.d8_completion_date = car.d7_completion_date + timedelta(days=1) if car.d7_completion_date else None
        car.d8_notes = "Team recognized for their contributions"


def generate_reports(db, audits):
    """Generate audit reports."""
    print("Generating audit reports...")

    report_types = ["Audit Report", "NC Summary", "CAR Status", "Management Review", "Executive Summary"]
    reports = []

    # Generate 10 reports
    for i, audit in enumerate(audits[:10]):
        if audit.status != "Completed":
            continue

        report_type = random.choice(report_types)

        report = AuditReport(
            report_number=f"RPT-{audit.actual_date.strftime('%Y%m%d')}-{i+1:03d}",
            audit_id=audit.id,
            report_type=report_type,
            summary=f"Comprehensive {report_type.lower()} for {audit.audit_number}",
            executive_summary=audit.executive_summary,
            findings_summary=f"Total findings: {audit.total_findings} (Major NC: {audit.major_nc_count}, Minor NC: {audit.minor_nc_count}, OFI: {audit.ofi_count})",
            recommendations=fake.paragraph(nb_sentences=4),
            pdf_path=f"data/sample_pdfs/{report_type.replace(' ', '_').lower()}_{audit.audit_number}.pdf",
            pdf_generated=datetime.now() - timedelta(days=random.randint(0, 30)),
            pdf_size_bytes=random.randint(100000, 500000),
            total_audits=1,
            total_nc=audit.major_nc_count + audit.minor_nc_count,
            total_ofi=audit.ofi_count,
            completion_rate=f"{audit.compliance_percentage:.1f}%" if audit.compliance_percentage else "N/A",
            average_score=f"{audit.overall_score:.1f}" if audit.overall_score else "N/A",
            generated_at=datetime.now() - timedelta(days=random.randint(0, 30)),
            generated_by=audit.lead_auditor,
            created_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )

        db.add(report)
        reports.append(report)

    db.commit()
    print(f"✅ Created {len(reports)} audit reports")
    return reports


def main():
    """Main function to generate all sample data."""
    print("=" * 60)
    print("Audit Pro Enterprise - Sample Data Generator")
    print("=" * 60)

    # Initialize database
    print("\nInitializing database...")
    init_db()
    print("✅ Database initialized")

    # Get database session
    db = get_db()

    try:
        # Generate data
        audits = generate_audits(db, count=24)
        nc_ofis = generate_nc_ofi(db, audits)
        cars = generate_cars(db, nc_ofis)
        reports = generate_reports(db, audits)

        print("\n" + "=" * 60)
        print("✅ SAMPLE DATA GENERATION COMPLETE")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  - Audits: {len(audits)}")
        print(f"  - NC/OFI: {len(nc_ofis)}")
        print(f"  - CARs (8D): {len(cars)}")
        print(f"    * Completed: {sum(1 for car in cars if car.status == 'Verified')}")
        print(f"    * In Progress: {sum(1 for car in cars if car.status != 'Verified')}")
        print(f"  - Reports: {len(reports)}")
        print(f"\n🚀 You can now run the application: streamlit run app.py")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error generating sample data: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()

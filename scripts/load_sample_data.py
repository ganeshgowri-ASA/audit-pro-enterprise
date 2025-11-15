"""
Load sample data for NC/OFI tracking system
Creates:
- 10 sample users
- 5 sample audits
- 15 NCs (5 Critical, 5 Major, 5 Minor)
- 10 OFIs
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import random

from database import SessionLocal, init_db
from models.user import User
from models.audit import Audit
from models.nc_ofi import NCOFI
from models.nc_ofi_history import NCOFIHistory

def load_sample_data():
    """Load sample data into database"""

    # Initialize database
    init_db()
    db = SessionLocal()

    # Check if data already exists
    if db.query(User).count() > 0:
        print("Sample data already exists. Skipping...")
        return

    print("Loading sample data...")

    # Create sample users
    users_data = [
        {"username": "john.doe", "email": "john.doe@example.com", "full_name": "John Doe", "department": "Quality", "role": "QA Manager"},
        {"username": "jane.smith", "email": "jane.smith@example.com", "full_name": "Jane Smith", "department": "Production", "role": "Production Manager"},
        {"username": "bob.johnson", "email": "bob.johnson@example.com", "full_name": "Bob Johnson", "department": "Engineering", "role": "Engineering Lead"},
        {"username": "alice.brown", "email": "alice.brown@example.com", "full_name": "Alice Brown", "department": "Quality", "role": "Quality Engineer"},
        {"username": "charlie.davis", "email": "charlie.davis@example.com", "full_name": "Charlie Davis", "department": "Operations", "role": "Operations Manager"},
        {"username": "diana.wilson", "email": "diana.wilson@example.com", "full_name": "Diana Wilson", "department": "Quality", "role": "Internal Auditor"},
        {"username": "edward.moore", "email": "edward.moore@example.com", "full_name": "Edward Moore", "department": "Production", "role": "Supervisor"},
        {"username": "fiona.taylor", "email": "fiona.taylor@example.com", "full_name": "Fiona Taylor", "department": "Engineering", "role": "Process Engineer"},
        {"username": "george.anderson", "email": "george.anderson@example.com", "full_name": "George Anderson", "department": "Quality", "role": "QA Specialist"},
        {"username": "hannah.thomas", "email": "hannah.thomas@example.com", "full_name": "Hannah Thomas", "department": "Operations", "role": "Operations Coordinator"}
    ]

    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)

    db.commit()
    print(f"✓ Created {len(users)} users")

    # Create sample audits
    audits_data = [
        {
            "audit_number": "AUD-2024-001",
            "audit_type": "Internal",
            "standard": "ISO 9001:2015",
            "department": "Production",
            "audit_date": datetime.now().date() - timedelta(days=60),
            "status": "Completed",
            "scope": "Production processes and quality control"
        },
        {
            "audit_number": "AUD-2024-002",
            "audit_type": "Internal",
            "standard": "IATF 16949:2016",
            "department": "Quality",
            "audit_date": datetime.now().date() - timedelta(days=45),
            "status": "Completed",
            "scope": "Quality management system effectiveness"
        },
        {
            "audit_number": "AUD-2024-003",
            "audit_type": "Supplier",
            "standard": "VDA 6.3",
            "department": "Purchasing",
            "audit_date": datetime.now().date() - timedelta(days=30),
            "status": "Completed",
            "scope": "Supplier process audit"
        },
        {
            "audit_number": "AUD-2024-004",
            "audit_type": "Internal",
            "standard": "ISO 9001:2015",
            "department": "Engineering",
            "audit_date": datetime.now().date() - timedelta(days=15),
            "status": "InProgress",
            "scope": "Design and development processes"
        },
        {
            "audit_number": "AUD-2024-005",
            "audit_type": "External",
            "standard": "IATF 16949:2016",
            "department": "All",
            "audit_date": datetime.now().date() - timedelta(days=7),
            "status": "InProgress",
            "scope": "Full system certification audit"
        }
    ]

    audits = []
    for audit_data in audits_data:
        audit_data['auditor_id'] = random.choice([u.id for u in users[:3]])
        audit_data['auditee_id'] = random.choice([u.id for u in users[3:]])
        audit = Audit(**audit_data)
        db.add(audit)
        audits.append(audit)

    db.commit()
    print(f"✓ Created {len(audits)} audits")

    # Create 15 NCs (5 Critical, 5 Major, 5 Minor)
    nc_descriptions = {
        "Critical": [
            "Product shipped without final inspection verification. Critical quality control process bypassed.",
            "Calibration records missing for critical measurement equipment. Potential impact on product conformity.",
            "Emergency exit blocked by stored materials. Immediate safety hazard identified.",
            "Traceability system failure - unable to track product batch to raw material lot. Critical tracking issue.",
            "Customer complaint process not followed - no root cause analysis performed for major defect."
        ],
        "Major": [
            "Work instructions outdated and not reflecting current process. Last revision 2 years ago.",
            "Training records incomplete for 3 operators on new production line.",
            "Internal audit schedule not maintained - 2 audits overdue by 3 months.",
            "Preventive maintenance not performed per schedule on critical equipment.",
            "Management review meeting minutes incomplete - missing action items and responsibilities."
        ],
        "Minor": [
            "Housekeeping issues in storage area - materials not properly identified.",
            "Document control procedure not followed - obsolete procedure found in work area.",
            "Temperature monitoring records have gaps - 2 days missing in past month.",
            "Personal protective equipment storage not organized - PPE scattered in multiple locations.",
            "Suggestion box not emptied regularly - suggestions from 2 months ago still unreviewed."
        ]
    }

    clauses_iso = ["4.4.1", "5.1.1", "6.2.1", "7.1.5", "7.5.3", "8.2.3", "8.5.1", "8.6", "9.1.2", "9.2", "9.3", "10.2"]

    ncs = []
    for severity in ["Critical", "Major", "Minor"]:
        for i, desc in enumerate(nc_descriptions[severity]):
            days_ago = random.randint(5, 60)
            created_date = datetime.now() - timedelta(days=days_ago)

            # Determine status based on age
            if days_ago > 45:
                status = random.choice(["Verified", "Closed"])
                closure_date = created_date.date() + timedelta(days=random.randint(20, 40))
            elif days_ago > 30:
                status = "InProgress"
                closure_date = None
            else:
                status = "Open"
                closure_date = None

            nc = NCOFI(
                audit_id=random.choice([a.id for a in audits]),
                type="NC",
                category=random.choice(["Major", "Minor", "Observation"]),
                severity=severity,
                clause_no=random.choice(clauses_iso),
                description=desc,
                status=status,
                assignee_id=random.choice([u.id for u in users]),
                due_date=created_date.date() + timedelta(days=30),
                closure_date=closure_date,
                created_at=created_date
            )
            db.add(nc)
            ncs.append(nc)

    db.commit()
    print(f"✓ Created {len(ncs)} NCs (5 Critical, 5 Major, 5 Minor)")

    # Create 10 OFIs
    ofi_descriptions = [
        "Implement automated data collection for production metrics to reduce manual entry errors.",
        "Consider upgrading to digital inspection checklists for faster data capture and analysis.",
        "Opportunity to streamline approval process by implementing electronic signature system.",
        "Suggestion to create visual management boards in production areas for real-time KPI tracking.",
        "Implement predictive maintenance program using equipment sensor data.",
        "Opportunity to cross-train operators on multiple production lines for better flexibility.",
        "Consider implementing 5S methodology in warehouse for improved organization.",
        "Develop supplier scorecard system for better supplier performance tracking.",
        "Opportunity to automate report generation for monthly quality metrics.",
        "Implement knowledge management system to capture and share best practices."
    ]

    ofis = []
    for i, desc in enumerate(ofi_descriptions):
        days_ago = random.randint(5, 45)
        created_date = datetime.now() - timedelta(days=days_ago)

        # OFIs typically have lower priority
        status = random.choice(["Open", "InProgress", "Closed"])
        if status == "Closed":
            closure_date = created_date.date() + timedelta(days=random.randint(15, 35))
        else:
            closure_date = None

        ofi = NCOFI(
            audit_id=random.choice([a.id for a in audits]),
            type="OFI",
            category="Observation",
            severity=random.choice(["Major", "Minor"]),
            clause_no=random.choice(clauses_iso),
            description=desc,
            status=status,
            assignee_id=random.choice([u.id for u in users]),
            due_date=created_date.date() + timedelta(days=60),  # Longer timeline for OFIs
            closure_date=closure_date,
            created_at=created_date
        )
        db.add(ofi)
        ofis.append(ofi)

    db.commit()
    print(f"✓ Created {len(ofis)} OFIs")

    # Create some history records for status changes
    all_findings = ncs + ofis
    for finding in all_findings:
        # Initial creation history
        history = NCOFIHistory(
            nc_ofi_id=finding.id,
            old_status=None,
            new_status="Open",
            comment="Finding created during audit",
            changed_at=finding.created_at
        )
        db.add(history)

        # Add status transition histories
        if finding.status == "InProgress":
            history = NCOFIHistory(
                nc_ofi_id=finding.id,
                old_status="Open",
                new_status="InProgress",
                comment="Root cause analysis initiated",
                changed_at=finding.created_at + timedelta(days=random.randint(3, 10))
            )
            db.add(history)

        elif finding.status == "Verified":
            history1 = NCOFIHistory(
                nc_ofi_id=finding.id,
                old_status="Open",
                new_status="InProgress",
                comment="Corrective action implemented",
                changed_at=finding.created_at + timedelta(days=random.randint(5, 15))
            )
            db.add(history1)

            history2 = NCOFIHistory(
                nc_ofi_id=finding.id,
                old_status="InProgress",
                new_status="Verified",
                comment="Effectiveness verified by Quality team",
                changed_at=finding.created_at + timedelta(days=random.randint(20, 30))
            )
            db.add(history2)

        elif finding.status == "Closed":
            history1 = NCOFIHistory(
                nc_ofi_id=finding.id,
                old_status="Open",
                new_status="InProgress",
                comment="Action plan developed",
                changed_at=finding.created_at + timedelta(days=random.randint(3, 10))
            )
            db.add(history1)

            history2 = NCOFIHistory(
                nc_ofi_id=finding.id,
                old_status="InProgress",
                new_status="Verified",
                comment="Actions verified effective",
                changed_at=finding.created_at + timedelta(days=random.randint(15, 25))
            )
            db.add(history2)

            history3 = NCOFIHistory(
                nc_ofi_id=finding.id,
                old_status="Verified",
                new_status="Closed",
                comment="Finding closed by management",
                changed_at=finding.created_at + timedelta(days=random.randint(25, 40))
            )
            db.add(history3)

    db.commit()
    print(f"✓ Created status history records")

    print("\n✅ Sample data loaded successfully!")
    print(f"\nSummary:")
    print(f"  - Users: {len(users)}")
    print(f"  - Audits: {len(audits)}")
    print(f"  - NCs: {len(ncs)} (Critical: 5, Major: 5, Minor: 5)")
    print(f"  - OFIs: {len(ofis)}")
    print(f"  - Total Findings: {len(all_findings)}")

    db.close()


if __name__ == "__main__":
    load_sample_data()

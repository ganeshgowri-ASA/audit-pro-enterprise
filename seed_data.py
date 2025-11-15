"""
Seed Data Script
AuditPro Enterprise - Populate database with sample data
"""

from config.database import init_db, get_session
from models.user import User
from models.entity import Entity
from models.audit import AuditType, AuditProgram
from models.checklist import Checklist, ChecklistItem
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_users(db):
    """Create sample users"""
    logger.info("Creating users...")

    users_data = [
        {
            "username": "admin",
            "email": "admin@auditpro.com",
            "password": "admin123",
            "full_name": "System Administrator",
            "employee_id": "EMP001",
            "department": "IT",
            "role": "Admin",
            "is_auditor": True
        },
        {
            "username": "auditor1",
            "email": "auditor1@auditpro.com",
            "password": "auditor123",
            "full_name": "John Auditor",
            "employee_id": "EMP002",
            "department": "Quality",
            "role": "Auditor",
            "is_auditor": True
        },
        {
            "username": "qm",
            "email": "qm@auditpro.com",
            "password": "qm123",
            "full_name": "Quality Manager",
            "employee_id": "EMP003",
            "department": "Quality",
            "role": "Quality Manager",
            "is_auditor": True
        },
        {
            "username": "user1",
            "email": "user1@auditpro.com",
            "password": "user123",
            "full_name": "Jane User",
            "employee_id": "EMP004",
            "department": "Production",
            "role": "User",
            "is_auditor": False
        }
    ]

    for user_data in users_data:
        # Check if user exists
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                employee_id=user_data["employee_id"],
                department=user_data["department"],
                role=user_data["role"],
                is_auditor=user_data["is_auditor"],
                is_active=True
            )
            user.set_password(user_data["password"])
            db.add(user)
            logger.info(f"Created user: {user_data['username']}")

    db.commit()
    logger.info("Users created successfully")


def seed_entities(db):
    """Create sample entities"""
    logger.info("Creating entities...")

    # Company
    company = Entity(
        code="COMP-001",
        name="AcmeCorp Manufacturing",
        entity_type="Company",
        description="Main company entity",
        manager_name="CEO Name",
        manager_email="ceo@acmecorp.com",
        location="Headquarters"
    )
    db.add(company)
    db.commit()

    # Plants
    plant1 = Entity(
        code="PLT-001",
        name="Plant North",
        entity_type="Plant",
        description="Northern manufacturing plant",
        manager_name="Plant Manager North",
        manager_email="pm.north@acmecorp.com",
        location="North Region",
        parent_id=company.id
    )
    db.add(plant1)
    db.commit()

    plant2 = Entity(
        code="PLT-002",
        name="Plant South",
        entity_type="Plant",
        description="Southern manufacturing plant",
        manager_name="Plant Manager South",
        manager_email="pm.south@acmecorp.com",
        location="South Region",
        parent_id=company.id
    )
    db.add(plant2)
    db.commit()

    # Departments under Plant North
    dept1 = Entity(
        code="DEPT-001",
        name="Production Department",
        entity_type="Department",
        description="Production operations",
        manager_name="Production Manager",
        manager_email="prod@acmecorp.com",
        location="Plant North - Building A",
        parent_id=plant1.id
    )
    db.add(dept1)

    dept2 = Entity(
        code="DEPT-002",
        name="Quality Department",
        entity_type="Department",
        description="Quality assurance and control",
        manager_name="Quality Manager",
        manager_email="quality@acmecorp.com",
        location="Plant North - Building B",
        parent_id=plant1.id
    )
    db.add(dept2)

    dept3 = Entity(
        code="DEPT-003",
        name="Logistics Department",
        entity_type="Department",
        description="Warehouse and shipping",
        manager_name="Logistics Manager",
        manager_email="logistics@acmecorp.com",
        location="Plant North - Building C",
        parent_id=plant1.id
    )
    db.add(dept3)

    db.commit()
    logger.info("Entities created successfully")


def seed_audit_types(db):
    """Create sample audit types"""
    logger.info("Creating audit types...")

    audit_types = [
        {
            "code": "INT-SYS",
            "name": "Internal System Audit",
            "description": "Systematic audit of QMS processes",
            "category": "Internal"
        },
        {
            "code": "INT-PROC",
            "name": "Internal Process Audit",
            "description": "Process-specific audit",
            "category": "Process"
        },
        {
            "code": "INT-PROD",
            "name": "Internal Product Audit",
            "description": "Product quality audit",
            "category": "Product"
        },
        {
            "code": "EXT-CERT",
            "name": "External Certification Audit",
            "description": "Third-party certification audit",
            "category": "External"
        },
        {
            "code": "SUP-EVAL",
            "name": "Supplier Evaluation Audit",
            "description": "Supplier quality assessment",
            "category": "Supplier"
        }
    ]

    for at_data in audit_types:
        existing = db.query(AuditType).filter(AuditType.code == at_data["code"]).first()
        if not existing:
            audit_type = AuditType(**at_data)
            db.add(audit_type)
            logger.info(f"Created audit type: {at_data['code']}")

    db.commit()
    logger.info("Audit types created successfully")


def seed_audit_programs(db):
    """Create sample audit programs"""
    logger.info("Creating audit programs...")

    current_year = date.today().year

    program = AuditProgram(
        year=current_year,
        name=f"Annual Audit Program {current_year}",
        description=f"Internal audit program for {current_year}",
        standard="ISO 9001:2015",
        status="Active"
    )
    db.add(program)
    db.commit()
    logger.info("Audit programs created successfully")


def seed_checklists(db):
    """Create sample checklists"""
    logger.info("Creating checklists...")

    # ISO 9001 checklist
    checklist = Checklist(
        code="ISO9001-CL001",
        name="ISO 9001:2015 - Clause 4 Context of Organization",
        description="Checklist for ISO 9001:2015 Clause 4",
        standard="ISO 9001",
        category="System",
        version="1.0",
        is_active=True
    )
    db.add(checklist)
    db.commit()

    # Checklist items
    items = [
        {
            "item_number": "4.1",
            "question": "Has the organization determined external and internal issues relevant to its purpose and strategic direction?",
            "requirement": "Organization must identify internal and external issues that affect QMS",
            "clause_reference": "ISO 9001:2015 - 4.1",
            "process_area": "Context of Organization",
            "criticality": "Major",
            "max_score": 5.0,
            "weight": 1.0,
            "sequence": 1
        },
        {
            "item_number": "4.2",
            "question": "Has the organization determined interested parties and their requirements relevant to the QMS?",
            "requirement": "Interested parties and their requirements must be identified",
            "clause_reference": "ISO 9001:2015 - 4.2",
            "process_area": "Context of Organization",
            "criticality": "Major",
            "max_score": 5.0,
            "weight": 1.0,
            "sequence": 2
        },
        {
            "item_number": "4.3",
            "question": "Has the organization determined the scope of the QMS?",
            "requirement": "QMS scope must be defined and documented",
            "clause_reference": "ISO 9001:2015 - 4.3",
            "process_area": "QMS Scope",
            "criticality": "Critical",
            "max_score": 5.0,
            "weight": 1.5,
            "sequence": 3
        },
        {
            "item_number": "4.4",
            "question": "Has the organization established, implemented, and maintained a QMS?",
            "requirement": "QMS must be established, documented, implemented and maintained",
            "clause_reference": "ISO 9001:2015 - 4.4",
            "process_area": "QMS Implementation",
            "criticality": "Critical",
            "max_score": 5.0,
            "weight": 2.0,
            "sequence": 4
        }
    ]

    for item_data in items:
        item = ChecklistItem(
            checklist_id=checklist.id,
            **item_data
        )
        db.add(item)

    db.commit()
    logger.info("Checklists created successfully")


def main():
    """Main seeding function"""
    logger.info("Starting database seeding...")

    # Initialize database
    init_db()

    # Get database session
    db = get_session()

    try:
        # Seed data
        seed_users(db)
        seed_entities(db)
        seed_audit_types(db)
        seed_audit_programs(db)
        seed_checklists(db)

        logger.info("Database seeding completed successfully!")

        # Print summary
        print("\n" + "="*60)
        print("DATABASE SEEDING SUMMARY")
        print("="*60)
        print(f"Users created: {db.query(User).count()}")
        print(f"Entities created: {db.query(Entity).count()}")
        print(f"Audit types created: {db.query(AuditType).count()}")
        print(f"Audit programs created: {db.query(AuditProgram).count()}")
        print(f"Checklists created: {db.query(Checklist).count()}")
        print(f"Checklist items created: {db.query(ChecklistItem).count()}")
        print("="*60)
        print("\nDefault Login Credentials:")
        print("Username: admin")
        print("Password: admin123")
        print("="*60)

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

"""
Unit Tests for Models
AuditPro Enterprise
"""

import pytest
from datetime import date
from config.database import init_db, get_session
from models.user import User
from models.entity import Entity
from models.audit import AuditType, AuditProgram
from models.checklist import Checklist, ChecklistItem


@pytest.fixture(scope="module")
def db_session():
    """Create database session for tests"""
    init_db()
    session = get_session()
    yield session
    session.close()


def test_user_creation(db_session):
    """Test user model creation and password hashing"""
    user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        employee_id="TEST001",
        role="User",
        is_active=True
    )
    user.set_password("password123")

    db_session.add(user)
    db_session.commit()

    # Test password checking
    assert user.check_password("password123") is True
    assert user.check_password("wrongpassword") is False

    # Cleanup
    db_session.delete(user)
    db_session.commit()


def test_entity_hierarchy(db_session):
    """Test entity hierarchy relationships"""
    # Create company
    company = Entity(
        code="TEST-COMP",
        name="Test Company",
        entity_type="Company",
        description="Test company entity"
    )
    db_session.add(company)
    db_session.commit()

    # Create plant under company
    plant = Entity(
        code="TEST-PLT",
        name="Test Plant",
        entity_type="Plant",
        description="Test plant entity",
        parent_id=company.id
    )
    db_session.add(plant)
    db_session.commit()

    # Test hierarchy
    assert plant.parent.id == company.id
    assert plant.get_hierarchy_level() == 1
    assert company.get_hierarchy_level() == 0
    assert "Test Company / Test Plant" in plant.get_full_path()

    # Cleanup
    db_session.delete(plant)
    db_session.delete(company)
    db_session.commit()


def test_audit_type_creation(db_session):
    """Test audit type creation"""
    audit_type = AuditType(
        code="TEST-AUDIT",
        name="Test Audit Type",
        description="Test audit type",
        category="Internal"
    )
    db_session.add(audit_type)
    db_session.commit()

    # Verify
    assert audit_type.id is not None
    assert audit_type.code == "TEST-AUDIT"

    # Cleanup
    db_session.delete(audit_type)
    db_session.commit()


def test_checklist_items(db_session):
    """Test checklist and items relationship"""
    # Create checklist
    checklist = Checklist(
        code="TEST-CL",
        name="Test Checklist",
        description="Test checklist",
        standard="ISO 9001",
        is_active=True
    )
    db_session.add(checklist)
    db_session.commit()

    # Create checklist items
    item1 = ChecklistItem(
        checklist_id=checklist.id,
        item_number="1.1",
        question="Test question 1?",
        requirement="Test requirement",
        max_score=5.0,
        sequence=1
    )
    item2 = ChecklistItem(
        checklist_id=checklist.id,
        item_number="1.2",
        question="Test question 2?",
        requirement="Test requirement",
        max_score=5.0,
        sequence=2
    )
    db_session.add_all([item1, item2])
    db_session.commit()

    # Verify relationship
    assert len(checklist.items) == 2

    # Cleanup
    db_session.delete(item1)
    db_session.delete(item2)
    db_session.delete(checklist)
    db_session.commit()


def test_base_model_timestamps(db_session):
    """Test that BaseModel timestamps are created"""
    entity = Entity(
        code="TIMESTAMP-TEST",
        name="Timestamp Test",
        entity_type="Company"
    )
    db_session.add(entity)
    db_session.commit()

    # Verify timestamps
    assert entity.created_at is not None
    assert entity.updated_at is not None
    assert entity.id is not None

    # Cleanup
    db_session.delete(entity)
    db_session.commit()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

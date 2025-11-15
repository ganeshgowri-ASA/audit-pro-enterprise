"""
Unit Tests for Database Configuration
AuditPro Enterprise
"""

import pytest
from config.database import init_db, get_session, get_db, Base, engine
from models.user import User


def test_database_initialization():
    """Test database initialization"""
    result = init_db()
    assert result is True


def test_database_connection():
    """Test database connection"""
    session = get_session()
    assert session is not None
    session.close()


def test_get_db_generator():
    """Test get_db generator function"""
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None

    # Close properly
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_session_operations():
    """Test basic CRUD operations"""
    session = get_session()

    try:
        # Create
        user = User(
            username="db_test_user",
            email="dbtest@example.com",
            full_name="DB Test User",
            role="User"
        )
        user.set_password("testpass")
        session.add(user)
        session.commit()

        # Read
        retrieved_user = session.query(User).filter(
            User.username == "db_test_user"
        ).first()
        assert retrieved_user is not None
        assert retrieved_user.email == "dbtest@example.com"

        # Update
        retrieved_user.full_name = "Updated Name"
        session.commit()

        updated_user = session.query(User).filter(
            User.username == "db_test_user"
        ).first()
        assert updated_user.full_name == "Updated Name"

        # Delete
        session.delete(updated_user)
        session.commit()

        deleted_user = session.query(User).filter(
            User.username == "db_test_user"
        ).first()
        assert deleted_user is None

    finally:
        session.close()


def test_transaction_rollback():
    """Test transaction rollback on error"""
    session = get_session()

    try:
        # Create user
        user = User(
            username="rollback_test",
            email="rollback@example.com",
            full_name="Rollback Test",
            role="User"
        )
        user.set_password("test")
        session.add(user)
        session.commit()

        # Intentionally cause an error
        user.username = None  # This should violate NOT NULL constraint
        try:
            session.commit()
        except Exception:
            session.rollback()

        # Verify rollback worked
        test_user = session.query(User).filter(
            User.email == "rollback@example.com"
        ).first()

        # User should still exist with original username
        if test_user:
            assert test_user.username == "rollback_test"
            session.delete(test_user)
            session.commit()

    finally:
        session.close()


def test_table_creation():
    """Test that all tables are created"""
    inspector = engine.dialect.get_inspector(engine.connect())
    table_names = inspector.get_table_names()

    # Check essential tables exist
    essential_tables = [
        'users',
        'entities',
        'audit_types',
        'audit_programs',
        'audits',
        'checklists',
        'checklist_items',
        'nc_ofi',
        'corrective_actions'
    ]

    for table in essential_tables:
        assert table in table_names, f"Table {table} was not created"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

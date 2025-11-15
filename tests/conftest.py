"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models.user import User
from models.audit import Audit
from models.nc_ofi import NCOFI
from models.nc_ofi_history import NCOFIHistory
from datetime import datetime, timedelta


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Create in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user"""
    user = User(
        username="testuser",
        email="testuser@example.com",
        full_name="Test User",
        department="Quality",
        role="QA Engineer"
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_audit(db_session, sample_user):
    """Create a sample audit"""
    audit = Audit(
        audit_number="TEST-001",
        audit_type="Internal",
        standard="ISO 9001:2015",
        department="Quality",
        auditor_id=sample_user.id,
        audit_date=datetime.now().date(),
        status="Completed"
    )
    db_session.add(audit)
    db_session.commit()
    return audit


@pytest.fixture
def sample_nc(db_session, sample_audit, sample_user):
    """Create a sample NC finding"""
    nc = NCOFI(
        audit_id=sample_audit.id,
        type="NC",
        category="Major",
        severity="Major",
        clause_no="8.5.1",
        description="Test non-conformity description",
        status="Open",
        assignee_id=sample_user.id,
        due_date=datetime.now().date() + timedelta(days=30)
    )
    db_session.add(nc)
    db_session.commit()
    return nc


@pytest.fixture
def sample_ofi(db_session, sample_audit, sample_user):
    """Create a sample OFI finding"""
    ofi = NCOFI(
        audit_id=sample_audit.id,
        type="OFI",
        category="Observation",
        severity="Minor",
        clause_no="9.1.2",
        description="Test opportunity for improvement description",
        status="Open",
        assignee_id=sample_user.id,
        due_date=datetime.now().date() + timedelta(days=60)
    )
    db_session.add(ofi)
    db_session.commit()
    return ofi

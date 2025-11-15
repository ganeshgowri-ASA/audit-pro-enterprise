"""
Pytest configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base
from models.entity import Entity


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test.
    Uses in-memory SQLite database.
    """
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_entities(db_session):
    """
    Create sample entity hierarchy for testing.

    Hierarchy:
    - Corporate (Level 0)
      - Plant A (Level 1)
        - Line 1 (Level 2)
          - Process 1 (Level 3)
        - Line 2 (Level 2)
      - Plant B (Level 1)
    """
    # Level 0 - Corporate
    corporate = Entity(
        name="Test Corp",
        type="Corporate",
        level=0,
        parent_id=None,
        is_active=True
    )
    db_session.add(corporate)
    db_session.flush()

    # Level 1 - Plants
    plant_a = Entity(
        name="Plant A",
        type="Plant",
        level=1,
        parent_id=corporate.id,
        is_active=True
    )
    plant_b = Entity(
        name="Plant B",
        type="Plant",
        level=1,
        parent_id=corporate.id,
        is_active=True
    )
    db_session.add_all([plant_a, plant_b])
    db_session.flush()

    # Level 2 - Lines
    line_1 = Entity(
        name="Line 1",
        type="Line",
        level=2,
        parent_id=plant_a.id,
        is_active=True
    )
    line_2 = Entity(
        name="Line 2",
        type="Line",
        level=2,
        parent_id=plant_a.id,
        is_active=True
    )
    db_session.add_all([line_1, line_2])
    db_session.flush()

    # Level 3 - Process
    process_1 = Entity(
        name="Process 1",
        type="Process",
        level=3,
        parent_id=line_1.id,
        is_active=True
    )
    db_session.add(process_1)
    db_session.flush()

    db_session.commit()

    return {
        "corporate": corporate,
        "plant_a": plant_a,
        "plant_b": plant_b,
        "line_1": line_1,
        "line_2": line_2,
        "process_1": process_1
    }

"""
Database configuration and session management for Audit Pro Enterprise.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

# Database URL - can be configured via environment variable
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./audit_pro.db')

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {},
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped session for thread-safety
db_session = scoped_session(SessionLocal)

# Base class for models
Base = declarative_base()


def init_db():
    """Initialize the database by creating all tables."""
    from models import audit, nc_ofi, car, reports  # Import all models
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session. Use with context manager."""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def reset_db():
    """Drop all tables and recreate them. USE WITH CAUTION!"""
    Base.metadata.drop_all(bind=engine)
    init_db()

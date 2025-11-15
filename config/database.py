"""
Database Configuration and Session Management
AuditPro Enterprise
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config.settings import DATABASE_URL
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped session for thread-safety
db_session = scoped_session(SessionLocal)

# Create declarative base
Base = declarative_base()


def get_db():
    """
    Get database session

    Usage:
        db = get_db()
        try:
            # Your database operations
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    """
    try:
        # Import all models here to ensure they are registered with Base
        from models import user, entity, audit, checklist, nc_ofi, car

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False


def reset_db():
    """
    Reset database - drop and recreate all tables
    WARNING: This will delete all data!
    """
    try:
        # Import all models
        from models import user, entity, audit, checklist, nc_ofi, car

        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped")

        # Recreate all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database reset successfully")
        return True
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        return False


def get_session():
    """
    Get a new database session
    Returns a session that should be closed after use
    """
    return SessionLocal()

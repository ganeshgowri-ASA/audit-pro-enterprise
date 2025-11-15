"""
Database session management
"""
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from database.engine import engine

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """
    Context manager for database sessions.
    Ensures proper cleanup of database connections.

    Usage:
        with get_db() as db:
            entities = db.query(Entity).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """
    Get a database session.
    Caller is responsible for closing the session.

    Returns:
        Session: SQLAlchemy session
    """
    return SessionLocal()

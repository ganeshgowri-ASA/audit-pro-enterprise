"""
Database initialization and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import Base, User
import os

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///audit_pro.db')

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {}
)

# Create session factory
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def init_database():
    """Initialize database tables."""
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")


def get_session():
    """Get a new database session."""
    return Session()


def close_session():
    """Close the current database session."""
    Session.remove()


# Export commonly used items
__all__ = ['engine', 'Session', 'get_session', 'close_session', 'init_database', 'User']

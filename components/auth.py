"""
Authentication and authorization component.
Handles user authentication, password hashing, and role-based access control.
"""
import bcrypt
import streamlit as st
from datetime import datetime
from models import get_session, User
from typing import Optional, Dict, Any


# Role hierarchy and permissions
ROLE_PERMISSIONS = {
    'admin': ['create', 'read', 'update', 'delete', 'manage_users', 'manage_audits', 'manage_findings', 'view_reports'],
    'auditor': ['create', 'read', 'update', 'manage_audits', 'manage_findings', 'view_reports'],
    'auditee': ['read', 'respond_findings', 'view_assigned_audits'],
    'viewer': ['read', 'view_reports']
}


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password as a string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password: Plain text password to verify
        password_hash: Stored password hash

    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def login(username: str, password: str, remember_me: bool = False) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with username and password.

    Args:
        username: User's username
        password: User's plain text password
        remember_me: Whether to persist session

    Returns:
        User dictionary if authentication successful, None otherwise
    """
    session = get_session()
    try:
        # Find user by username
        user = session.query(User).filter(User.username == username).first()

        if not user:
            print(f"Login failed: User '{username}' not found")
            return None

        # Check if user is active
        if not user.is_active:
            print(f"Login failed: User '{username}' is inactive")
            return None

        # Verify password
        if not verify_password(password, user.password_hash):
            print(f"Login failed: Invalid password for user '{username}'")
            return None

        # Update last login time
        user.last_login = datetime.utcnow()
        session.commit()

        # Store user in session state
        user_dict = user.to_dict()
        st.session_state['authenticated'] = True
        st.session_state['user'] = user_dict
        st.session_state['remember_me'] = remember_me

        print(f"Login successful: User '{username}' logged in as '{user.role}'")
        return user_dict

    except Exception as e:
        print(f"Login error: {e}")
        session.rollback()
        return None
    finally:
        session.close()


def logout():
    """
    Log out the current user by clearing session state.
    """
    if 'user' in st.session_state:
        username = st.session_state['user'].get('username', 'Unknown')
        print(f"Logout: User '{username}' logged out")

    # Clear authentication session state
    st.session_state['authenticated'] = False
    st.session_state['user'] = None
    st.session_state['remember_me'] = False


def check_authentication() -> bool:
    """
    Check if a user is currently authenticated.

    Returns:
        True if user is authenticated, False otherwise
    """
    return st.session_state.get('authenticated', False) and st.session_state.get('user') is not None


def get_current_user() -> Optional[Dict[str, Any]]:
    """
    Get the currently authenticated user.

    Returns:
        User dictionary if authenticated, None otherwise
    """
    if check_authentication():
        return st.session_state.get('user')
    return None


def check_permission(permission: str, user: Optional[Dict[str, Any]] = None) -> bool:
    """
    Check if the current user has a specific permission.

    Args:
        permission: Permission to check (e.g., 'create', 'delete', 'manage_users')
        user: User dictionary (optional, uses current user if not provided)

    Returns:
        True if user has permission, False otherwise
    """
    if user is None:
        user = get_current_user()

    if not user:
        return False

    role = user.get('role')
    if not role:
        return False

    permissions = ROLE_PERMISSIONS.get(role, [])
    return permission in permissions


def check_role(role: str, user: Optional[Dict[str, Any]] = None) -> bool:
    """
    Check if the current user has a specific role.

    Args:
        role: Role to check (e.g., 'admin', 'auditor')
        user: User dictionary (optional, uses current user if not provided)

    Returns:
        True if user has the role, False otherwise
    """
    if user is None:
        user = get_current_user()

    if not user:
        return False

    return user.get('role') == role


def require_authentication(func):
    """
    Decorator to require authentication for a function.
    Redirects to login page if not authenticated.
    """
    def wrapper(*args, **kwargs):
        if not check_authentication():
            st.warning("Please log in to access this page.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_permission(permission: str):
    """
    Decorator to require a specific permission for a function.
    Shows error if user doesn't have permission.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_authentication():
                st.error("Please log in to access this page.")
                st.stop()
            if not check_permission(permission):
                st.error(f"You don't have permission to access this feature. Required permission: {permission}")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role: str):
    """
    Decorator to require a specific role for a function.
    Shows error if user doesn't have the role.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_authentication():
                st.error("Please log in to access this page.")
                st.stop()
            if not check_role(role):
                st.error(f"You don't have permission to access this feature. Required role: {role}")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_user_permissions(user: Optional[Dict[str, Any]] = None) -> list:
    """
    Get list of permissions for a user.

    Args:
        user: User dictionary (optional, uses current user if not provided)

    Returns:
        List of permission strings
    """
    if user is None:
        user = get_current_user()

    if not user:
        return []

    role = user.get('role')
    return ROLE_PERMISSIONS.get(role, [])

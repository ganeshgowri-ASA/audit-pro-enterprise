"""
Authentication Component
AuditPro Enterprise - User authentication and session management
"""

import streamlit as st
from config.database import get_session
from models.user import User
from datetime import datetime, timedelta
from config.settings import SESSION_EXPIRY_HOURS


def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "login_time" not in st.session_state:
        st.session_state.login_time = None


def check_session_expiry():
    """Check if session has expired"""
    if st.session_state.authenticated and st.session_state.login_time:
        session_duration = datetime.now() - st.session_state.login_time
        if session_duration > timedelta(hours=SESSION_EXPIRY_HOURS):
            logout()
            return True
    return False


def login(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate user

    Args:
        username: Username or email
        password: Plain text password

    Returns:
        tuple: (success: bool, message: str)
    """
    db = get_session()
    try:
        # Find user by username or email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()

        if not user:
            return False, "Invalid username or password"

        if not user.is_active:
            return False, "Account is inactive. Please contact administrator."

        if not user.check_password(password):
            return False, "Invalid username or password"

        # Set session state
        st.session_state.authenticated = True
        st.session_state.user = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "department": user.department,
            "is_auditor": user.is_auditor
        }
        st.session_state.login_time = datetime.now()

        return True, f"Welcome, {user.full_name}!"

    except Exception as e:
        return False, f"Login error: {str(e)}"
    finally:
        db.close()


def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_time = None


def require_auth(func):
    """
    Decorator to require authentication for a page

    Usage:
        @require_auth
        def my_page():
            st.write("Protected content")
    """
    def wrapper(*args, **kwargs):
        init_session_state()

        if check_session_expiry():
            st.warning("Session expired. Please login again.")
            show_login_page()
            return

        if not st.session_state.authenticated:
            show_login_page()
            return

        return func(*args, **kwargs)
    return wrapper


def require_role(allowed_roles: list):
    """
    Decorator to require specific role(s)

    Usage:
        @require_role(["Admin", "Quality Manager"])
        def admin_page():
            st.write("Admin content")
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            init_session_state()

            if not st.session_state.authenticated:
                show_login_page()
                return

            if st.session_state.user["role"] not in allowed_roles:
                st.error(f"Access denied. Required roles: {', '.join(allowed_roles)}")
                st.info(f"Your role: {st.session_state.user['role']}")
                return

            return func(*args, **kwargs)
        return wrapper
    return decorator


def show_login_page():
    """Display login page"""
    st.title("AuditPro Enterprise")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                success, message = login(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    # Information
    st.markdown("---")
    st.info("""
    **AuditPro Enterprise**
    Enterprise Audit Management System
    ISO 9001, IATF 16949, VDA 6.3 Compliant

    **Default Credentials:**
    Username: `admin`
    Password: `admin123`
    """)


def get_current_user():
    """
    Get current logged-in user info

    Returns:
        dict: User information or None
    """
    if st.session_state.authenticated:
        return st.session_state.user
    return None


def is_admin():
    """Check if current user is admin"""
    user = get_current_user()
    return user and user["role"] == "Admin"


def is_auditor():
    """Check if current user is auditor"""
    user = get_current_user()
    return user and (user["is_auditor"] or user["role"] in ["Admin", "Auditor"])


def show_user_info():
    """Display current user info in sidebar"""
    if st.session_state.authenticated:
        user = st.session_state.user
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Logged in as:**  \n{user['full_name']}")
        st.sidebar.markdown(f"**Role:** {user['role']}")
        if st.sidebar.button("Logout", use_container_width=True):
            logout()
            st.rerun()

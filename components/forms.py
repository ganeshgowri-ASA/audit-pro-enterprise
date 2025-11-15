"""
Reusable Form Components
AuditPro Enterprise - Common form elements and inputs
"""

import streamlit as st
from datetime import date, timedelta
from config.settings import AUDIT_STATUSES, NC_SEVERITIES, NC_STATUSES, CAR_STATUSES, STANDARDS, USER_ROLES


def date_input_with_default(label: str, default_days_offset: int = 0, key: str = None):
    """
    Date input with default value

    Args:
        label: Input label
        default_days_offset: Days to add to today (can be negative)
        key: Unique key for the widget

    Returns:
        date: Selected date
    """
    default_date = date.today() + timedelta(days=default_days_offset)
    return st.date_input(label, value=default_date, key=key)


def entity_selector(label: str = "Select Entity", key: str = None, required: bool = True):
    """
    Entity selection dropdown

    Args:
        label: Dropdown label
        key: Unique key
        required: If True, shows validation

    Returns:
        int: Selected entity ID or None
    """
    from config.database import get_session
    from models.entity import Entity

    db = get_session()
    try:
        entities = db.query(Entity).order_by(Entity.name).all()
        entity_options = {f"{e.code} - {e.name}": e.id for e in entities}

        if not entity_options:
            st.warning("No entities found. Please create entities first.")
            return None

        options = [""] + list(entity_options.keys()) if not required else list(entity_options.keys())
        selected = st.selectbox(label, options, key=key)

        if selected and selected in entity_options:
            return entity_options[selected]
        return None
    finally:
        db.close()


def user_selector(label: str = "Select User", key: str = None, role_filter: str = None, required: bool = True):
    """
    User selection dropdown

    Args:
        label: Dropdown label
        key: Unique key
        role_filter: Filter by role (e.g., "Auditor")
        required: If True, shows validation

    Returns:
        int: Selected user ID or None
    """
    from config.database import get_session
    from models.user import User

    db = get_session()
    try:
        query = db.query(User).filter(User.is_active == True)

        if role_filter == "Auditor":
            query = query.filter(User.is_auditor == True)
        elif role_filter:
            query = query.filter(User.role == role_filter)

        users = query.order_by(User.full_name).all()
        user_options = {f"{u.full_name} ({u.username})": u.id for u in users}

        if not user_options:
            st.warning(f"No {role_filter or ''} users found.")
            return None

        options = [""] + list(user_options.keys()) if not required else list(user_options.keys())
        selected = st.selectbox(label, options, key=key)

        if selected and selected in user_options:
            return user_options[selected]
        return None
    finally:
        db.close()


def audit_type_selector(label: str = "Select Audit Type", key: str = None):
    """
    Audit type selection dropdown

    Returns:
        int: Selected audit type ID or None
    """
    from config.database import get_session
    from models.audit import AuditType

    db = get_session()
    try:
        audit_types = db.query(AuditType).order_by(AuditType.name).all()
        type_options = {f"{at.code} - {at.name}": at.id for at in audit_types}

        if not type_options:
            st.warning("No audit types found. Please create audit types first.")
            return None

        selected = st.selectbox(label, list(type_options.keys()), key=key)
        if selected:
            return type_options[selected]
        return None
    finally:
        db.close()


def status_badge(status: str, status_colors: dict = None):
    """
    Display colored status badge

    Args:
        status: Status text
        status_colors: Dictionary mapping status to color
    """
    default_colors = {
        "Open": "red",
        "In Progress": "orange",
        "Completed": "green",
        "Closed": "blue",
        "Verified": "green",
        "Cancelled": "gray",
        "Planned": "blue",
        "Active": "green",
        "Draft": "gray"
    }

    colors = status_colors or default_colors
    color = colors.get(status, "gray")

    st.markdown(
        f'<span style="background-color: {color}; color: white; padding: 0.25rem 0.5rem; '
        f'border-radius: 0.25rem; font-size: 0.875rem;">{status}</span>',
        unsafe_allow_html=True
    )


def severity_badge(severity: str):
    """
    Display colored severity badge

    Args:
        severity: Severity level
    """
    colors = {
        "Critical": "#d32f2f",
        "Major": "#f57c00",
        "Minor": "#fbc02d",
        "Observation": "#0288d1"
    }

    color = colors.get(severity, "#757575")

    st.markdown(
        f'<span style="background-color: {color}; color: white; padding: 0.25rem 0.5rem; '
        f'border-radius: 0.25rem; font-size: 0.875rem; font-weight: bold;">{severity}</span>',
        unsafe_allow_html=True
    )


def confirmation_dialog(message: str, key: str = "confirm"):
    """
    Simple confirmation dialog

    Args:
        message: Confirmation message
        key: Unique key

    Returns:
        bool: True if confirmed
    """
    with st.expander("⚠️ Confirm Action", expanded=True):
        st.warning(message)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Confirm", key=f"{key}_yes", use_container_width=True):
                return True
        with col2:
            if st.button("✗ Cancel", key=f"{key}_no", use_container_width=True):
                return False
    return None


def success_message(message: str, duration: int = 3):
    """
    Display success message

    Args:
        message: Success message
        duration: Display duration in seconds
    """
    st.success(message)


def error_message(message: str):
    """
    Display error message

    Args:
        message: Error message
    """
    st.error(message)


def info_card(title: str, value: str, icon: str = "📊"):
    """
    Display information card

    Args:
        title: Card title
        value: Value to display
        icon: Icon to show
    """
    st.markdown(f"""
    <div style="padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem; margin: 0.5rem 0;">
        <div style="font-size: 2rem;">{icon}</div>
        <div style="font-size: 0.875rem; color: #666;">{title}</div>
        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.25rem;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

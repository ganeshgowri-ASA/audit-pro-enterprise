"""
Main Streamlit application with authentication.
Enterprise Audit Management System - ISO 9001, IATF 16949, VDA 6.3 compliant.
"""
import streamlit as st
from components.auth import (
    check_authentication,
    get_current_user,
    logout,
    get_user_permissions
)
from pages.login import show_login_page

# Page configuration
st.set_page_config(
    page_title="Audit Pro Enterprise",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None


def show_sidebar():
    """Display sidebar with user info and logout button."""
    with st.sidebar:
        st.title("📋 Audit Pro Enterprise")
        st.divider()

        if check_authentication():
            user = get_current_user()
            if user:
                st.success(f"Logged in as: **{user['username']}**")
                st.info(f"Role: **{user['role'].title()}**")

                if user.get('full_name'):
                    st.caption(f"👤 {user['full_name']}")
                if user.get('department'):
                    st.caption(f"🏢 {user['department']}")

                st.divider()

                # Show user permissions
                with st.expander("🔐 My Permissions"):
                    permissions = get_user_permissions(user)
                    for perm in permissions:
                        st.caption(f"✓ {perm.replace('_', ' ').title()}")

                st.divider()

                # Logout button
                if st.button("🚪 Logout", use_container_width=True):
                    logout()
                    st.rerun()


def show_home_page():
    """Display home page for authenticated users."""
    user = get_current_user()

    st.title("🏠 Welcome to Audit Pro Enterprise")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Your Role", user['role'].title())

    with col2:
        if user.get('department'):
            st.metric("Department", user['department'])
        else:
            st.metric("Department", "Not Set")

    with col3:
        permissions = get_user_permissions(user)
        st.metric("Permissions", len(permissions))

    st.markdown("---")

    st.subheader("📊 System Overview")
    st.info("""
    **Audit Pro Enterprise** is a comprehensive audit management system designed for:

    - ISO 9001 Quality Management
    - IATF 16949 Automotive Quality
    - VDA 6.3 Process Audits
    - NC/OFI Tracking
    - CAR/8D Management
    - Audit Planning & Reporting
    """)

    st.markdown("---")

    st.subheader("🎯 Quick Actions")

    action_col1, action_col2, action_col3, action_col4 = st.columns(4)

    with action_col1:
        if st.button("📝 New Audit", use_container_width=True):
            st.info("Audit module coming soon...")

    with action_col2:
        if st.button("📋 My Audits", use_container_width=True):
            st.info("Audit list module coming soon...")

    with action_col3:
        if st.button("📊 Reports", use_container_width=True):
            st.info("Reports module coming soon...")

    with action_col4:
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("Settings module coming soon...")

    st.markdown("---")

    # Role-specific features
    st.subheader("🔑 Available Features")

    if user['role'] == 'admin':
        st.success("""
        **Administrator Features:**
        - Full system access
        - User management
        - System configuration
        - All audit operations
        - Complete reporting access
        """)
    elif user['role'] == 'auditor':
        st.info("""
        **Auditor Features:**
        - Create and manage audits
        - View all audit data
        - Manage findings
        - Generate reports
        """)
    elif user['role'] == 'auditee':
        st.warning("""
        **Auditee Features:**
        - View assigned audits
        - Respond to findings
        - Track corrective actions
        """)
    elif user['role'] == 'viewer':
        st.info("""
        **Viewer Features:**
        - Read-only access
        - View audits and reports
        - Export data
        """)


def main():
    """Main application entry point."""
    # Show sidebar
    show_sidebar()

    # Check authentication
    if not check_authentication():
        show_login_page()
    else:
        show_home_page()


if __name__ == "__main__":
    main()

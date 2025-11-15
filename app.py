"""
AuditPro Enterprise - Main Application
Multi-page Streamlit app for enterprise audit management
"""

import streamlit as st
from components.auth import init_session_state, require_auth, show_user_info, get_current_user
from config.database import init_db
from config.settings import APP_NAME, APP_VERSION, APP_DESCRIPTION
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def initialize_database():
    """Initialize database on first run"""
    return init_db()

# Initialize
init_session_state()
initialize_database()


@require_auth
def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        st.title(APP_NAME)
        st.caption(f"Version {APP_VERSION}")
        st.markdown("---")

        # Navigation
        st.subheader("Navigation")

        # User info
        show_user_info()

    # Main content
    st.title("Dashboard")
    st.markdown(f"**{APP_DESCRIPTION}**")
    st.markdown("---")

    # Welcome message
    user = get_current_user()
    st.header(f"Welcome, {user['full_name']}!")

    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Audits",
            value="0",
            delta="This Year"
        )

    with col2:
        st.metric(
            label="Open NC/OFI",
            value="0",
            delta="-0 from last month"
        )

    with col3:
        st.metric(
            label="Active CARs",
            value="0",
            delta="In Progress"
        )

    with col4:
        st.metric(
            label="Compliance Score",
            value="0%",
            delta="+0%"
        )

    st.markdown("---")

    # Quick Actions
    st.subheader("Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 New Audit", use_container_width=True):
            st.info("Navigate to Audit Execution page to create a new audit")

    with col2:
        if st.button("⚠️ Report NC/OFI", use_container_width=True):
            st.info("Navigate to NC/OFI Tracking page to report findings")

    with col3:
        if st.button("🔧 Create CAR", use_container_width=True):
            st.info("Navigate to Corrective Actions page to create a CAR")

    st.markdown("---")

    # Recent Activity
    st.subheader("Recent Activity")
    st.info("No recent activity to display. Start by creating entities and users.")

    # System Information
    with st.expander("System Information"):
        st.markdown(f"""
        **Application:** {APP_NAME}
        **Version:** {APP_VERSION}
        **Description:** {APP_DESCRIPTION}

        **Current User:**
        - Name: {user['full_name']}
        - Role: {user['role']}
        - Department: {user.get('department', 'N/A')}

        **Database:** SQLite (initialized)

        **Available Modules:**
        - ✅ Authentication & User Management
        - ✅ Entity Management
        - 📋 Audit Planning (Coming Soon)
        - ✅ Audit Execution (Coming Soon)
        - ⚠️ NC/OFI Tracking (Coming Soon)
        - 🔧 Corrective Actions (Coming Soon)
        - 📊 Reports & Analytics (Coming Soon)
        """)

    # Help section
    with st.expander("Need Help?"):
        st.markdown("""
        **Getting Started:**
        1. Create organizational entities (Company → Plant → Department)
        2. Set up users and assign roles
        3. Define audit types and programs
        4. Create checklists
        5. Start conducting audits

        **Navigation:**
        - Use the sidebar to navigate between modules
        - Dashboard provides overview and quick actions
        - Each module has dedicated functionality

        **Default Credentials:**
        - Username: `admin`
        - Password: `admin123`

        **Note:** This is the base structure setup. Additional modules will be implemented in subsequent sessions.
        """)


if __name__ == "__main__":
    main()

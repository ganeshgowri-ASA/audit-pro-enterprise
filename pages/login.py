"""
Login page for Audit Pro Enterprise.
Handles user authentication with username/password.
"""
import streamlit as st
from components.auth import login


def show_login_page():
    """Display the login page."""
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("# 🔐 Login")
        st.markdown("### Audit Pro Enterprise")
        st.markdown("---")

        # Login form
        with st.form("login_form", clear_on_submit=False):
            st.markdown("#### Enter your credentials")

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            remember_me = st.checkbox(
                "Remember me",
                value=False,
                key="login_remember"
            )

            submit_button = st.form_submit_button(
                "🚀 Login",
                use_container_width=True
            )

            if submit_button:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    # Attempt login
                    user = login(username, password, remember_me)

                    if user:
                        st.success(f"Welcome back, {user['full_name'] or user['username']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")

        st.markdown("---")

        # Demo credentials info
        with st.expander("ℹ️ Demo Credentials"):
            st.markdown("""
            **Administrator:**
            - Username: `admin`
            - Password: `admin123`

            **Auditor:**
            - Username: `auditor1`
            - Password: `audit123`

            **Auditee:**
            - Username: `auditee1`
            - Password: `auditee123`

            **Viewer:**
            - Username: `viewer1`
            - Password: `view123`
            """)

        # System info
        st.caption("🔒 Secure authentication with bcrypt password hashing")
        st.caption("📋 ISO 9001, IATF 16949, VDA 6.3 Compliant")

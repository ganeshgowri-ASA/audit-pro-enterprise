"""
Audit Pro Enterprise - Main Application
Enterprise Audit Management System with CAR/8D and Reporting
"""
import streamlit as st
from database import init_db

# Page configuration
st.set_page_config(
    page_title="Audit Pro Enterprise",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on first run
@st.cache_resource
def initialize_database():
    """Initialize database tables."""
    try:
        init_db()
        return True
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        return False

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database
if initialize_database():
    # Main page header
    st.markdown('<div class="main-header">🔍 Audit Pro Enterprise</div>', unsafe_allow_html=True)

    # Welcome section
    st.markdown("""
    ### Welcome to Audit Pro Enterprise

    A comprehensive enterprise audit management system supporting:
    - **ISO 9001** - Quality Management Systems
    - **IATF 16949** - Automotive Quality Management
    - **VDA 6.3** - Process Audit
    """)

    # Key features
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>📋 Audit Management</h4>
        <ul>
        <li>Plan and schedule audits</li>
        <li>Track audit execution</li>
        <li>Document findings</li>
        <li>Manage NC/OFI</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>🔧 CAR & 8D System</h4>
        <ul>
        <li>8D methodology workflow</li>
        <li>Root cause analysis</li>
        <li>5-Why analysis</li>
        <li>Fishbone diagrams</li>
        <li>Effectiveness verification</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-box">
        <h4>📊 Reports & Analytics</h4>
        <ul>
        <li>Executive dashboards</li>
        <li>PDF report generation</li>
        <li>Trend analysis</li>
        <li>KPI tracking</li>
        <li>Data export (Excel/CSV)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Quick statistics (placeholder)
    st.markdown("---")
    st.subheader("📈 Quick Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">Total Audits</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">Open NC/OFI</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">Active CARs</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">0%</div>
        <div class="metric-label">Completion Rate</div>
        </div>
        """, unsafe_allow_html=True)

    # Navigation guide
    st.markdown("---")
    st.markdown("""
    ### 🧭 Navigation

    Use the sidebar to navigate between different modules:

    1. **🔧 Corrective Actions** - Manage CARs with 8D methodology
    2. **📊 Reports & Analytics** - View dashboards and generate reports

    ---

    **Getting Started:**
    1. Generate sample data using the data generation script: `python utils/generate_sample_data.py`
    2. Navigate to Corrective Actions to create and manage CARs
    3. View analytics and generate reports in the Reports & Analytics module

    **Support:** For issues or questions, refer to the README.md file
    """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
    <small>Audit Pro Enterprise v1.0 | Built with Streamlit | © 2024</small>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Failed to initialize database. Please check your configuration.")

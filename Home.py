"""
Audit Pro Enterprise - Home Page

Enterprise Audit Management System with Entity Hierarchy Management
"""
import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Audit Pro Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏢 Audit Pro Enterprise</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Comprehensive Entity Hierarchy Management System</div>', unsafe_allow_html=True)

# Check if database is initialized
db_path = Path("audit_pro.db")
db_exists = db_path.exists()

if not db_exists:
    st.warning("⚠️ Database not initialized. Please run the initialization script first.")

    st.markdown("### 🚀 Getting Started")

    st.code("""
# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python scripts/init_db.py

# Run the application
streamlit run Home.py
    """, language="bash")

    st.info("After initialization, refresh this page to access the application.")
    st.stop()

# Welcome section
st.markdown("## 👋 Welcome")

st.markdown("""
This enterprise-grade audit management system provides comprehensive tools for managing
organizational hierarchies, conducting audits, and ensuring compliance with international
standards including ISO 9001, IATF 16949, and VDA 6.3.
""")

# Features overview
st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🏢 Entity Management</h3>
        <ul>
            <li>Hierarchical organization structure</li>
            <li>5-level hierarchy support</li>
            <li>Circular reference prevention</li>
            <li>Active/Inactive status tracking</li>
            <li>Excel export capabilities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🔍 Advanced Search</h3>
        <ul>
            <li>Multi-criteria filtering</li>
            <li>Full-text search</li>
            <li>Level-based filtering</li>
            <li>Type-based categorization</li>
            <li>Real-time results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Data Management</h3>
        <ul>
            <li>CRUD operations</li>
            <li>Relationship validation</li>
            <li>Data integrity checks</li>
            <li>Audit trail (timestamps)</li>
            <li>Bulk operations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Entity hierarchy levels
st.markdown("## 🏗️ Organizational Hierarchy")

st.markdown("""
The system supports a 5-level hierarchical structure to represent complex organizational layouts:
""")

levels_col1, levels_col2 = st.columns(2)

with levels_col1:
    st.markdown("""
    ### Hierarchy Levels
    - **Level 0: Corporate** - Top-level organization
    - **Level 1: Plant** - Manufacturing facilities
    - **Level 2: Line** - Production/assembly lines
    - **Level 3: Process** - Individual processes
    - **Level 4: Sub-Process** - Process components
    """)

with levels_col2:
    st.markdown("""
    ### Example Structure
    ```
    ABC Corporation (Corporate)
    ├── Plant A - Mumbai (Plant)
    │   ├── Assembly Line 1 (Line)
    │   │   ├── Welding Process (Process)
    │   │   └── Painting Process (Process)
    │   └── Assembly Line 2 (Line)
    └── Plant B - Pune (Plant)
        └── Quality Control Line (Line)
            └── Inspection Process (Process)
    ```
    """)

# Quick stats (if database exists)
try:
    from database.session import get_db
    from models.entity import Entity
    from utils.entity_helpers import get_entity_statistics

    st.markdown("## 📊 System Overview")

    with get_db() as db:
        stats = get_entity_statistics(db)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Entities", stats['total'], help="Total number of entities in the system")

    with col2:
        st.metric("Active Entities", stats['active'], help="Currently active entities")

    with col3:
        st.metric("Inactive Entities", stats['inactive'], help="Deactivated entities")

    with col4:
        hierarchy_depth = max([level for level, count in stats['by_type'].items() if count > 0] or [0],
                             default=0, key=lambda x: list(stats['by_type'].keys()).index(x) if x in stats['by_type'].keys() else -1)
        st.metric("Hierarchy Depth", f"{len([c for c in stats['by_type'].values() if c > 0])} levels",
                 help="Number of hierarchy levels in use")

    # Distribution by type
    st.markdown("### Distribution by Entity Type")

    type_cols = st.columns(5)
    for idx, (entity_type, count) in enumerate(stats['by_type'].items()):
        with type_cols[idx]:
            st.metric(entity_type, count)

except Exception as e:
    st.error(f"Error loading statistics: {str(e)}")

# Getting started guide
st.markdown("## 🚀 Getting Started")

st.markdown("""
### Navigation
Use the sidebar to navigate between different sections:
- **🏢 Entity Management** - Manage organizational hierarchy

### Quick Actions
1. **Add Entity** - Create new organizational units
2. **View Hierarchy** - Browse the hierarchical tree structure
3. **Search & Filter** - Find specific entities
4. **Export Data** - Download entity data to Excel

### Best Practices
- Start by creating top-level (Corporate) entities
- Ensure parent-child relationships follow the hierarchy levels
- Use descriptive names and locations for easy identification
- Maintain active/inactive status for historical tracking
- Regular data exports for backup purposes
""")

# System information
st.markdown("## ℹ️ System Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    **Version:** 1.0.0
    **Database:** SQLite (Production-ready)
    **Framework:** Streamlit
    **ORM:** SQLAlchemy 2.0
    """)

with info_col2:
    st.markdown("""
    **Standards Support:**
    - ISO 9001:2015
    - IATF 16949
    - VDA 6.3
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>🏢 Audit Pro Enterprise - Entity Hierarchy Management System</p>
    <p>Built with ❤️ using Streamlit and SQLAlchemy</p>
    <p style="font-size: 0.8rem;">© 2024 - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Quick Links")
    st.markdown("- [Entity Management](./01_🏢_Entity_Management)")

    st.divider()

    st.markdown("### 🔧 System Tools")
    if st.button("🔄 Refresh Statistics", use_container_width=True):
        st.rerun()

    st.divider()

    st.markdown("### 📖 Documentation")
    st.markdown("""
    **Key Concepts:**
    - Hierarchical Structure
    - Entity Relationships
    - Data Validation
    - Circular Reference Prevention
    """)

    st.divider()

    st.info("""
    **Need Help?**

    Check the Entity Management page for detailed instructions on managing your organizational hierarchy.
    """)

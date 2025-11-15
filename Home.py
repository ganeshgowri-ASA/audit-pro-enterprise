"""
Audit Pro Enterprise - Main Application
ISO 9001, IATF 16949, VDA 6.3 Compliant Audit Management System
"""
import streamlit as st
from database import init_db

# Page configuration
st.set_page_config(
    page_title="Audit Pro Enterprise",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Main page
st.title("📋 Audit Pro Enterprise")
st.markdown("### Enterprise Audit Management System")

st.markdown("""
Welcome to **Audit Pro Enterprise** - Your comprehensive solution for managing audits,
non-conformities, and opportunities for improvement in compliance with:

- **ISO 9001:2015** - Quality Management Systems
- **IATF 16949:2016** - Automotive Quality Management
- **VDA 6.3** - Process Audit

---

## 🎯 Key Features

### ⚠️ NC/OFI Tracking System
Track and manage Non-Conformities (NCs) and Opportunities for Improvement (OFIs) with:
- **Finding Creation** - Document findings with detailed information
- **Severity Classification** - Critical, Major, Minor severity levels
- **Assignment & Workflow** - Assign to responsible persons with due dates
- **Status Tracking** - Open → InProgress → Verified → Closed workflow
- **Aging Analysis** - Monitor how long findings remain open
- **Overdue Alerts** - Red highlighting for overdue items
- **Advanced Filtering** - By status, severity, assignee, and more
- **Search Capabilities** - Find by clause number or description
- **Excel Export** - Export findings data for reporting
- **Email Notifications** - Auto-notify assignees of new findings
- **Trend Analysis** - Visualize open vs closed findings over time
- **Bulk Operations** - Assign multiple findings at once

### 📊 Analytics & Reporting
- Real-time dashboards with KPIs
- Aging analysis of open findings
- Trend charts for continuous improvement
- Assignee workload distribution
- Status and severity breakdowns

### 🔔 Notifications & Alerts
- Automatic email notifications for assignments
- Overdue finding alerts
- Status change tracking with history

---

## 🚀 Getting Started

### For New Users:

1. **Navigate to NC/OFI Tracking** using the sidebar
2. **Explore the Dashboard** to see current statistics
3. **View Findings List** to see all tracked items
4. **Create New Findings** when issues are identified during audits
5. **Manage Status Updates** as findings progress through resolution

### Quick Actions:

- 📝 **Create Finding** - Document new NCs or OFIs
- 📊 **View Dashboard** - See real-time statistics
- 📈 **Analytics** - Track trends and performance
- 📥 **Export Data** - Generate Excel reports

---

## 📖 System Overview

The NC/OFI Tracking System helps organizations:
- **Identify** quality issues and improvement opportunities
- **Document** findings with full traceability
- **Assign** accountability to responsible personnel
- **Track** progress through resolution
- **Verify** effectiveness of corrective actions
- **Analyze** trends for continuous improvement

### Status Workflow:

```
Open → InProgress → Verified → Closed
```

- **Open**: Finding documented, awaiting action
- **InProgress**: Root cause analysis and corrective action underway
- **Verified**: Actions implemented and effectiveness verified
- **Closed**: Finding fully resolved and closed by management

---

## 💡 Sample Data

The system includes sample data to help you explore features:
- 10 Sample Users across different departments
- 5 Sample Audits (Internal, External, Supplier)
- 15 Non-Conformities (5 Critical, 5 Major, 5 Minor)
- 10 Opportunities for Improvement
- Complete status history and transitions

To load sample data, run:
```bash
python scripts/load_sample_data.py
```

---

## 🛠️ Configuration

System configuration can be customized in `.env` file:
- Database connection
- Email/SMTP settings for notifications
- Application preferences

---

## 📞 Support

For assistance or questions about the system, please contact your system administrator.

---

**Version:** 1.0.0
**Last Updated:** 2024
**Compliance:** ISO 9001:2015, IATF 16949:2016, VDA 6.3
""")

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📋 Navigation")
    st.markdown("""
    Use the pages above to navigate:

    - **⚠️ NC/OFI Tracking** - Main tracking system

    More modules coming soon:
    - Audit Planning
    - CAR/8D Management
    - Document Control
    - User Management
    """)

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")

    try:
        from database import SessionLocal
        from models.nc_ofi import NCOFI

        db = SessionLocal()

        total_findings = db.query(NCOFI).count()
        open_findings = db.query(NCOFI).filter(NCOFI.status.in_(["Open", "InProgress"])).count()
        closed_findings = db.query(NCOFI).filter(NCOFI.status == "Closed").count()

        st.metric("Total Findings", total_findings)
        st.metric("Open/InProgress", open_findings)
        st.metric("Closed", closed_findings)

        db.close()

    except Exception as e:
        st.info("Load sample data to see statistics")

    st.markdown("---")
    st.markdown("*Audit Pro Enterprise v1.0*")

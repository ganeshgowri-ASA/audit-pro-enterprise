"""
NC/OFI Tracking Page
Non-Conformity and Opportunity for Improvement Tracking System
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy.orm import Session

# Import models and utilities
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db
from models.nc_ofi import NCOFI
from models.nc_ofi_history import NCOFIHistory
from models.user import User
from models.audit import Audit
from utils.email_utils import send_nc_ofi_assignment_email
from utils.export_utils import export_nc_ofi_to_excel, prepare_findings_for_export
from utils.analytics_utils import (
    get_nc_ofi_statistics,
    get_aging_analysis,
    get_trend_data,
    get_assignee_workload
)
import config

# Page configuration
st.set_page_config(
    page_title="NC/OFI Tracking",
    page_icon="⚠️",
    layout="wide"
)

# Initialize database
init_db()

# Custom CSS for styling
st.markdown("""
<style>
    .overdue-row {
        background-color: #ffcccc !important;
    }
    .critical-severity {
        color: #ff0000;
        font-weight: bold;
    }
    .major-severity {
        color: #ff8800;
        font-weight: bold;
    }
    .minor-severity {
        color: #0066cc;
    }
    .status-open {
        background-color: #ffcccc;
        padding: 3px 8px;
        border-radius: 3px;
    }
    .status-inprogress {
        background-color: #fff3cd;
        padding: 3px 8px;
        border-radius: 3px;
    }
    .status-verified {
        background-color: #d1ecf1;
        padding: 3px 8px;
        border-radius: 3px;
    }
    .status-closed {
        background-color: #d4edda;
        padding: 3px 8px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚠️ NC/OFI Tracking System")
st.markdown("Non-Conformity & Opportunity for Improvement Management")

# Get database session
db = SessionLocal()

# Sidebar filters
st.sidebar.header("Filters")

# Get filter options
all_statuses = config.STATUS_WORKFLOW
all_severities = config.SEVERITY_LEVELS
all_types = config.NC_OFI_TYPES
all_users = db.query(User).all()
user_names = ["All"] + [u.full_name for u in all_users]

# Filter controls
filter_status = st.sidebar.multiselect(
    "Status",
    options=all_statuses,
    default=all_statuses
)

filter_severity = st.sidebar.multiselect(
    "Severity",
    options=all_severities,
    default=all_severities
)

filter_type = st.sidebar.multiselect(
    "Type",
    options=all_types,
    default=all_types
)

filter_assignee = st.sidebar.selectbox(
    "Assignee",
    options=user_names
)

show_overdue_only = st.sidebar.checkbox("Show Overdue Only")

# Search
search_term = st.sidebar.text_input("Search (Clause/Description)")

st.sidebar.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "📝 Findings List",
    "➕ Create Finding",
    "📈 Analytics"
])

# TAB 1: DASHBOARD
with tab1:
    st.header("Dashboard Overview")

    # Get statistics
    stats = get_nc_ofi_statistics(db, NCOFI)

    # Display KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Findings", stats['total_findings'])

    with col2:
        st.metric("Non-Conformities", stats['total_nc'])

    with col3:
        st.metric("OFIs", stats['total_ofi'])

    with col4:
        st.metric(
            "Overdue",
            stats['overdue_count'],
            delta=None,
            delta_color="inverse"
        )

    with col5:
        st.metric("Avg Days to Close", stats['avg_days_to_close'])

    st.markdown("---")

    # Status and Severity breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Status Breakdown")
        status_df = pd.DataFrame(
            list(stats['status_counts'].items()),
            columns=['Status', 'Count']
        )
        fig_status = px.pie(
            status_df,
            values='Count',
            names='Status',
            color='Status',
            color_discrete_map={
                'Open': '#dc3545',
                'InProgress': '#ffc107',
                'Verified': '#17a2b8',
                'Closed': '#28a745'
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        st.subheader("Severity Breakdown")
        severity_df = pd.DataFrame(
            list(stats['severity_counts'].items()),
            columns=['Severity', 'Count']
        )
        fig_severity = px.bar(
            severity_df,
            x='Severity',
            y='Count',
            color='Severity',
            color_discrete_map={
                'Critical': '#dc3545',
                'Major': '#fd7e14',
                'Minor': '#007bff'
            }
        )
        st.plotly_chart(fig_severity, use_container_width=True)

    # Aging Analysis
    st.subheader("Aging Analysis (Open Findings)")
    aging_data = get_aging_analysis(db, NCOFI)
    aging_df = pd.DataFrame(
        list(aging_data.items()),
        columns=['Age Bucket', 'Count']
    )

    fig_aging = px.bar(
        aging_df,
        x='Age Bucket',
        y='Count',
        color='Count',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_aging, use_container_width=True)

# TAB 2: FINDINGS LIST
with tab2:
    st.header("Findings List")

    # Build query with filters
    query = db.query(NCOFI)

    if filter_status:
        query = query.filter(NCOFI.status.in_(filter_status))

    if filter_severity:
        query = query.filter(NCOFI.severity.in_(filter_severity))

    if filter_type:
        query = query.filter(NCOFI.type.in_(filter_type))

    if filter_assignee != "All":
        user = db.query(User).filter(User.full_name == filter_assignee).first()
        if user:
            query = query.filter(NCOFI.assignee_id == user.id)

    if search_term:
        query = query.filter(
            (NCOFI.clause_no.contains(search_term)) |
            (NCOFI.description.contains(search_term))
        )

    findings = query.order_by(NCOFI.created_at.desc()).all()

    # Filter overdue if checkbox is checked
    if show_overdue_only:
        findings = [f for f in findings if f.is_overdue]

    st.write(f"**{len(findings)} findings found**")

    # Bulk operations
    if findings:
        col1, col2, col3 = st.columns([2, 2, 6])

        with col1:
            if st.button("📥 Export to Excel"):
                findings_data = prepare_findings_for_export(findings, db)
                excel_file = export_nc_ofi_to_excel(findings_data)

                st.download_button(
                    label="Download Excel",
                    data=excel_file,
                    file_name=f"nc_ofi_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        with col2:
            bulk_assign = st.checkbox("Bulk Assign")

        if bulk_assign:
            with st.form("bulk_assign_form"):
                st.write("Select findings to assign:")
                selected_ids = []

                for finding in findings[:10]:  # Limit to first 10 for demo
                    if st.checkbox(f"ID {finding.id}: {finding.type} - {finding.clause_no}", key=f"bulk_{finding.id}"):
                        selected_ids.append(finding.id)

                bulk_assignee = st.selectbox(
                    "Assign to",
                    options=[u.full_name for u in all_users]
                )

                if st.form_submit_button("Assign Selected"):
                    assignee = db.query(User).filter(User.full_name == bulk_assignee).first()
                    if assignee:
                        for finding_id in selected_ids:
                            finding = db.query(NCOFI).get(finding_id)
                            finding.assignee_id = assignee.id
                            db.commit()

                            # Send email notification
                            send_nc_ofi_assignment_email(finding, assignee)

                        st.success(f"Assigned {len(selected_ids)} findings to {bulk_assignee}")
                        st.rerun()

    # Display findings table
    if findings:
        for finding in findings:
            with st.expander(
                f"{'🔴' if finding.is_overdue else '🟢'} "
                f"[{finding.type}] ID-{finding.id} | {finding.severity} | "
                f"{finding.clause_no} | {finding.status}",
                expanded=False
            ):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"**ID:** {finding.id}")
                    st.write(f"**Type:** {finding.type}")
                    st.write(f"**Category:** {finding.category}")
                    st.write(f"**Severity:** {finding.severity}")

                with col2:
                    st.write(f"**Clause:** {finding.clause_no}")
                    st.write(f"**Status:** {finding.status}")
                    st.write(f"**Assignee:** {finding.assignee.full_name if finding.assignee else 'Unassigned'}")
                    st.write(f"**Audit:** {finding.audit.audit_number if finding.audit else 'N/A'}")

                with col3:
                    st.write(f"**Created:** {finding.created_at.strftime('%Y-%m-%d')}")
                    st.write(f"**Due Date:** {finding.due_date.strftime('%Y-%m-%d') if finding.due_date else 'Not set'}")
                    st.write(f"**Days Open:** {finding.days_open}")
                    if finding.is_overdue:
                        st.error(f"⚠️ OVERDUE by {abs(finding.days_until_due)} days")

                st.write(f"**Description:** {finding.description}")

                if finding.evidence_path:
                    st.write(f"**Evidence:** {finding.evidence_path}")

                # Status change form
                with st.form(f"status_form_{finding.id}"):
                    st.write("**Update Status:**")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        new_status = st.selectbox(
                            "New Status",
                            options=config.STATUS_WORKFLOW,
                            index=config.STATUS_WORKFLOW.index(finding.status),
                            key=f"status_{finding.id}"
                        )

                    with col2:
                        if new_status in ["Verified", "Closed"]:
                            closure_date = st.date_input(
                                "Closure Date",
                                value=datetime.now().date(),
                                key=f"closure_{finding.id}"
                            )
                        else:
                            closure_date = None

                    with col3:
                        comment = st.text_area(
                            "Comment",
                            key=f"comment_{finding.id}"
                        )

                    if st.form_submit_button("Update Status"):
                        old_status = finding.status
                        finding.status = new_status

                        if closure_date and new_status in ["Verified", "Closed"]:
                            finding.closure_date = closure_date

                        # Create history record
                        history = NCOFIHistory(
                            nc_ofi_id=finding.id,
                            old_status=old_status,
                            new_status=new_status,
                            comment=comment
                        )
                        db.add(history)
                        db.commit()

                        st.success(f"Status updated: {old_status} → {new_status}")
                        st.rerun()

                # Show history
                if finding.history:
                    st.write("**Status History:**")
                    for hist in reversed(finding.history):
                        st.text(
                            f"{hist.changed_at.strftime('%Y-%m-%d %H:%M')} | "
                            f"{hist.old_status} → {hist.new_status} | "
                            f"{hist.comment if hist.comment else 'No comment'}"
                        )
    else:
        st.info("No findings match the current filters.")

# TAB 3: CREATE FINDING
with tab3:
    st.header("Create New Finding")

    with st.form("create_finding_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Get audits for dropdown
            audits = db.query(Audit).all()
            audit_options = {f"{a.audit_number} - {a.audit_type}": a.id for a in audits}

            if audits:
                selected_audit = st.selectbox(
                    "Audit *",
                    options=list(audit_options.keys())
                )
                audit_id = audit_options[selected_audit]
            else:
                st.warning("No audits available. Please create an audit first.")
                audit_id = None

            finding_type = st.selectbox(
                "Type *",
                options=config.NC_OFI_TYPES
            )

            category = st.selectbox(
                "Category",
                options=config.NC_CATEGORIES
            )

            severity = st.selectbox(
                "Severity *",
                options=config.SEVERITY_LEVELS
            )

            clause_no = st.text_input(
                "Clause Number *",
                placeholder="e.g., 8.5.1"
            )

        with col2:
            assignee_name = st.selectbox(
                "Assignee *",
                options=[u.full_name for u in all_users]
            )

            due_date = st.date_input(
                "Due Date *",
                value=datetime.now().date() + timedelta(days=30)
            )

            status = st.selectbox(
                "Initial Status",
                options=config.STATUS_WORKFLOW,
                index=0
            )

            evidence_path = st.text_input(
                "Evidence Path",
                placeholder="/path/to/evidence"
            )

        description = st.text_area(
            "Description *",
            placeholder="Detailed description of the finding...",
            height=150
        )

        submit_button = st.form_submit_button("Create Finding")

        if submit_button:
            if not audit_id:
                st.error("Please select an audit.")
            elif not clause_no or not description:
                st.error("Please fill in all required fields (*)")
            else:
                # Get assignee
                assignee = db.query(User).filter(User.full_name == assignee_name).first()

                # Create new finding
                new_finding = NCOFI(
                    audit_id=audit_id,
                    type=finding_type,
                    category=category,
                    severity=severity,
                    clause_no=clause_no,
                    description=description,
                    status=status,
                    assignee_id=assignee.id if assignee else None,
                    due_date=due_date,
                    evidence_path=evidence_path if evidence_path else None
                )

                db.add(new_finding)
                db.commit()
                db.refresh(new_finding)

                # Create initial history record
                history = NCOFIHistory(
                    nc_ofi_id=new_finding.id,
                    old_status=None,
                    new_status=status,
                    comment="Finding created"
                )
                db.add(history)
                db.commit()

                # Send email notification
                if assignee:
                    send_nc_ofi_assignment_email(new_finding, assignee)

                st.success(f"✅ Finding created successfully! ID: {new_finding.id}")
                st.balloons()

# TAB 4: ANALYTICS
with tab4:
    st.header("Analytics & Trends")

    # Trend analysis
    st.subheader("Trend Analysis (Last 30 Days)")

    trend_df = get_trend_data(db, NCOFI, days=30)

    if not trend_df.empty:
        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
            x=trend_df['date'],
            y=trend_df['created'],
            mode='lines+markers',
            name='Total Created',
            line=dict(color='blue')
        ))

        fig_trend.add_trace(go.Scatter(
            x=trend_df['date'],
            y=trend_df['closed'],
            mode='lines+markers',
            name='Total Closed',
            line=dict(color='green')
        ))

        fig_trend.add_trace(go.Scatter(
            x=trend_df['date'],
            y=trend_df['open'],
            mode='lines+markers',
            name='Open Balance',
            line=dict(color='red')
        ))

        fig_trend.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode='x unified'
        )

        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No trend data available.")

    # Assignee workload
    st.subheader("Assignee Workload")

    workload_data = get_assignee_workload(db, NCOFI)

    if workload_data:
        workload_df = pd.DataFrame(workload_data)

        fig_workload = px.bar(
            workload_df,
            x='assignee',
            y=['open', 'in_progress', 'closed'],
            title='Findings by Assignee and Status',
            labels={'value': 'Count', 'assignee': 'Assignee'},
            barmode='stack'
        )

        st.plotly_chart(fig_workload, use_container_width=True)

        # Display table
        st.dataframe(workload_df, use_container_width=True)
    else:
        st.info("No workload data available.")

# Close database session
db.close()

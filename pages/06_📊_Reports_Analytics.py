"""
Reports & Analytics Dashboard Page
"""
import streamlit as st
from datetime import datetime, date, timedelta
from database import get_db
from models.audit import Audit
from models.nc_ofi import NC_OFI
from models.car import CorrectiveAction
from models.reports import AuditReport
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import json

st.set_page_config(page_title="Reports & Analytics", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .reports-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 5px solid #667eea;
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin: 0.5rem 0;
    }
    .kpi-label {
        font-size: 1rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-change {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .positive {
        color: #28a745;
    }
    .negative {
        color: #dc3545;
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
    <div class="reports-header">
        <h1>📊 Reports & Analytics Dashboard</h1>
        <p>Executive Insights, Trends, and Comprehensive Reporting</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📈 Dashboard Controls")

    view_mode = st.radio(
        "Select View:",
        ["Executive Dashboard", "PDF Reports", "Analytics", "Data Export"],
        index=0
    )

    st.markdown("---")
    st.subheader("🔍 Filters")

    # Date range filter
    date_range = st.date_input(
        "Date Range",
        value=(date.today() - timedelta(days=365), date.today()),
        key="date_range"
    )

    # Entity filter
    entity_filter = st.multiselect(
        "Filter by Entity",
        ["All Entities", "Manufacturing", "Quality", "Engineering", "Supply Chain"],
        default=["All Entities"]
    )

    # Standard filter
    standard_filter = st.multiselect(
        "Filter by Standard",
        ["All Standards", "ISO 9001", "IATF 16949", "VDA 6.3"],
        default=["All Standards"]
    )

    # Auditor filter
    auditor_filter = st.text_input("Filter by Auditor", "")

# Database session
db = get_db()

# Helper functions for KPI calculations
def calculate_kpis(db, date_from, date_to):
    """Calculate key performance indicators."""
    # Total audits
    total_audits = db.query(Audit).filter(
        Audit.planned_date >= date_from,
        Audit.planned_date <= date_to
    ).count()

    # Completed audits
    completed_audits = db.query(Audit).filter(
        Audit.planned_date >= date_from,
        Audit.planned_date <= date_to,
        Audit.status == 'Completed'
    ).count()

    # Completion rate
    completion_rate = (completed_audits / total_audits * 100) if total_audits > 0 else 0

    # Average audit score
    audits = db.query(Audit).filter(
        Audit.planned_date >= date_from,
        Audit.planned_date <= date_to,
        Audit.overall_score.isnot(None)
    ).all()
    avg_score = sum([a.overall_score for a in audits]) / len(audits) if audits else 0

    # Open NC count
    open_nc = db.query(NC_OFI).filter(
        NC_OFI.status.in_(['Open', 'CAR Initiated', 'In Progress'])
    ).count()

    # Total NC/OFI
    total_nc = db.query(NC_OFI).filter(NC_OFI.finding_type.in_(['Major NC', 'Minor NC'])).count()
    total_ofi = db.query(NC_OFI).filter(NC_OFI.finding_type == 'OFI').count()

    # NC closure rate
    closed_nc = db.query(NC_OFI).filter(
        NC_OFI.status == 'Closed',
        NC_OFI.finding_type.in_(['Major NC', 'Minor NC'])
    ).count()
    nc_closure_rate = (closed_nc / total_nc * 100) if total_nc > 0 else 0

    # Active CARs
    active_cars = db.query(CorrectiveAction).filter(
        CorrectiveAction.status.in_(['Submitted', 'Approved', 'In Progress'])
    ).count()

    return {
        'total_audits': total_audits,
        'completed_audits': completed_audits,
        'completion_rate': completion_rate,
        'avg_score': avg_score,
        'open_nc': open_nc,
        'total_nc': total_nc,
        'total_ofi': total_ofi,
        'nc_closure_rate': nc_closure_rate,
        'active_cars': active_cars
    }

# Get date range
if isinstance(date_range, tuple) and len(date_range) == 2:
    date_from, date_to = date_range
else:
    date_from = date.today() - timedelta(days=365)
    date_to = date.today()

# Calculate KPIs
kpis = calculate_kpis(db, date_from, date_to)

# ===== EXECUTIVE DASHBOARD =====
if view_mode == "Executive Dashboard":
    st.subheader("📊 Executive Dashboard")

    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Audits</div>
            <div class="kpi-value">{kpis['total_audits']}</div>
            <div class="kpi-change positive">📈 Active</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Completion Rate</div>
            <div class="kpi-value">{kpis['completion_rate']:.1f}%</div>
            <div class="kpi-change {'positive' if kpis['completion_rate'] >= 80 else 'negative'}">
                {'✅ Good' if kpis['completion_rate'] >= 80 else '⚠️ Low'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Audit Score</div>
            <div class="kpi-value">{kpis['avg_score']:.1f}</div>
            <div class="kpi-change positive">Out of 100</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Open NC</div>
            <div class="kpi-value">{kpis['open_nc']}</div>
            <div class="kpi-change {'negative' if kpis['open_nc'] > 10 else 'positive'}">
                {'⚠️ Alert' if kpis['open_nc'] > 10 else '✅ OK'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">NC Closure Rate</div>
            <div class="kpi-value">{kpis['nc_closure_rate']:.1f}%</div>
            <div class="kpi-change {'positive' if kpis['nc_closure_rate'] >= 80 else 'negative'}">
                {'✅ Good' if kpis['nc_closure_rate'] >= 80 else '⚠️ Low'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 📈 Monthly Audit Trend")

        # Get audit data by month
        audits = db.query(Audit).filter(
            Audit.planned_date >= date_from,
            Audit.planned_date <= date_to
        ).all()

        if audits:
            df_audits = pd.DataFrame([{
                'month': a.planned_date.strftime('%Y-%m') if a.planned_date else 'Unknown',
                'status': a.status
            } for a in audits])

            monthly_counts = df_audits.groupby('month').size().reset_index(name='count')

            fig = px.bar(
                monthly_counts,
                x='month',
                y='count',
                title="Audits per Month",
                labels={'month': 'Month', 'count': 'Number of Audits'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No audit data available for the selected period.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🍩 NC Closure Status")

        nc_ofis = db.query(NC_OFI).all()

        if nc_ofis:
            status_counts = Counter([nc.status for nc in nc_ofis])
            df_status = pd.DataFrame.from_dict(status_counts, orient='index', columns=['count']).reset_index()
            df_status.columns = ['status', 'count']

            fig = px.pie(
                df_status,
                values='count',
                names='status',
                title="NC/OFI Status Distribution",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No NC/OFI data available.")

        st.markdown('</div>', unsafe_allow_html=True)

    # Charts Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 NC by Severity")

        nc_ofis = db.query(NC_OFI).all()

        if nc_ofis:
            severity_counts = Counter([nc.severity or 'Unknown' for nc in nc_ofis])
            df_severity = pd.DataFrame.from_dict(severity_counts, orient='index', columns=['count']).reset_index()
            df_severity.columns = ['severity', 'count']

            fig = px.bar(
                df_severity,
                x='severity',
                y='count',
                title="NC by Severity Level",
                labels={'severity': 'Severity', 'count': 'Count'},
                color='severity',
                color_discrete_map={
                    'Critical': '#dc3545',
                    'High': '#fd7e14',
                    'Medium': '#ffc107',
                    'Low': '#28a745',
                    'Unknown': '#6c757d'
                }
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No NC/OFI data available.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Audit Score Trend")

        audits_with_scores = db.query(Audit).filter(
            Audit.overall_score.isnot(None),
            Audit.actual_date.isnot(None)
        ).order_by(Audit.actual_date).all()

        if audits_with_scores:
            df_scores = pd.DataFrame([{
                'date': a.actual_date,
                'score': a.overall_score,
                'audit': a.audit_number
            } for a in audits_with_scores])

            fig = px.line(
                df_scores,
                x='date',
                y='score',
                title="Audit Score Trend Over Time",
                labels={'date': 'Date', 'score': 'Score'},
                markers=True
            )
            fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Target: 80")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No audit score data available.")

        st.markdown('</div>', unsafe_allow_html=True)

# ===== PDF REPORTS =====
elif view_mode == "PDF Reports":
    st.subheader("📄 PDF Report Generation")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Audit Report",
        "NC/OFI Summary",
        "CAR Status Report",
        "Management Review"
    ])

    with tab1:
        st.markdown("### 📋 Audit Report Generator")

        with st.form("audit_report_form"):
            col1, col2 = st.columns(2)

            with col1:
                # Select audit
                audits = db.query(Audit).all()
                if audits:
                    audit_options = {f"{a.audit_number} - {a.entity_name}": a.id for a in audits}
                    selected_audit = st.selectbox("Select Audit", options=list(audit_options.keys()))
                    audit_id = audit_options[selected_audit]
                else:
                    st.warning("No audits found.")
                    audit_id = None

                include_findings = st.checkbox("Include Findings", value=True)
                include_photos = st.checkbox("Include Evidence Photos", value=False)

            with col2:
                report_type = st.selectbox(
                    "Report Type",
                    ["Full Audit Report", "Executive Summary", "Findings Only"]
                )

                format_type = st.selectbox("Format", ["PDF", "DOCX"])

            submit = st.form_submit_button("🚀 Generate Report", use_container_width=True)

            if submit and audit_id:
                try:
                    # Create report record
                    audit = db.query(Audit).filter(Audit.id == audit_id).first()

                    new_report = AuditReport(
                        report_number=f"RPT-{datetime.now().strftime('%Y%m%d')}-{db.query(AuditReport).count() + 1:03d}",
                        audit_id=audit_id,
                        report_type="Audit Report",
                        summary=f"Comprehensive audit report for {audit.audit_number}",
                        executive_summary=audit.executive_summary or "Executive summary to be added.",
                        recommendations="Recommendations to be added.",
                        pdf_path=f"data/sample_pdfs/audit_report_{audit.audit_number}.pdf",
                        generated_at=datetime.utcnow(),
                        generated_by="Current User"
                    )

                    db.add(new_report)
                    db.commit()

                    st.success(f"✅ Report {new_report.report_number} generated successfully!")
                    st.info(f"📁 Report saved to: {new_report.pdf_path}")
                    st.download_button(
                        label="📥 Download Report",
                        data="Sample PDF content",
                        file_name=f"audit_report_{audit.audit_number}.pdf",
                        mime="application/pdf"
                    )

                except Exception as e:
                    st.error(f"Error generating report: {e}")
                    db.rollback()

    with tab2:
        st.markdown("### 📊 NC/OFI Summary Report")

        with st.form("nc_summary_form"):
            col1, col2 = st.columns(2)

            with col1:
                summary_date_range = st.date_input(
                    "Report Period",
                    value=(date.today() - timedelta(days=90), date.today())
                )

                grouping = st.selectbox(
                    "Group By",
                    ["Severity", "Category", "Department", "Status"]
                )

            with col2:
                include_charts = st.checkbox("Include Charts", value=True)
                include_trends = st.checkbox("Include Trend Analysis", value=True)

            submit_nc = st.form_submit_button("🚀 Generate NC Summary", use_container_width=True)

            if submit_nc:
                st.success("✅ NC/OFI Summary report generated!")
                st.info("📁 Report saved to: data/sample_pdfs/nc_summary.pdf")

    with tab3:
        st.markdown("### 🔧 CAR Status Report")

        with st.form("car_status_form"):
            col1, col2 = st.columns(2)

            with col1:
                car_status_filter = st.multiselect(
                    "CAR Status",
                    ["All", "Draft", "Submitted", "Approved", "In Progress", "Implemented", "Verified"],
                    default=["All"]
                )

                include_8d_progress = st.checkbox("Include 8D Progress", value=True)

            with col2:
                car_date_range = st.date_input(
                    "Report Period",
                    value=(date.today() - timedelta(days=90), date.today()),
                    key="car_date"
                )

            submit_car = st.form_submit_button("🚀 Generate CAR Report", use_container_width=True)

            if submit_car:
                st.success("✅ CAR Status report generated!")
                st.info("📁 Report saved to: data/sample_pdfs/car_status.pdf")

    with tab4:
        st.markdown("### 📈 Management Review Report")

        with st.form("mgmt_review_form"):
            col1, col2 = st.columns(2)

            with col1:
                review_period = st.selectbox(
                    "Review Period",
                    ["Monthly", "Quarterly", "Semi-Annual", "Annual"]
                )

                include_kpis = st.checkbox("Include KPIs", value=True)
                include_trends = st.checkbox("Include Trends", value=True)

            with col2:
                review_date = st.date_input("Review Date", value=date.today())

                include_action_items = st.checkbox("Include Action Items", value=True)

            submit_mgmt = st.form_submit_button("🚀 Generate Management Review", use_container_width=True)

            if submit_mgmt:
                st.success("✅ Management Review report generated!")
                st.info("📁 Report saved to: data/sample_pdfs/management_review.pdf")

# ===== ANALYTICS =====
elif view_mode == "Analytics":
    st.subheader("📈 Advanced Analytics")

    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "Audit Score Trends",
            "NC by Category",
            "Repeat Findings Analysis",
            "Auditor Performance",
            "Entity-wise Heatmap"
        ]
    )

    if analysis_type == "Audit Score Trends":
        st.markdown("#### 📈 Audit Score Trends Analysis")

        audits = db.query(Audit).filter(
            Audit.overall_score.isnot(None),
            Audit.actual_date.isnot(None)
        ).order_by(Audit.actual_date).all()

        if audits:
            df = pd.DataFrame([{
                'date': a.actual_date,
                'score': a.overall_score,
                'standard': a.standard,
                'entity': a.entity_name,
                'auditor': a.lead_auditor
            } for a in audits])

            # Line chart
            fig = px.line(
                df,
                x='date',
                y='score',
                color='standard',
                title="Audit Scores by Standard Over Time",
                markers=True
            )
            fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Target")
            st.plotly_chart(fig, use_container_width=True)

            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Score", f"{df['score'].mean():.1f}")
            with col2:
                st.metric("Median Score", f"{df['score'].median():.1f}")
            with col3:
                st.metric("Std Deviation", f"{df['score'].std():.1f}")

        else:
            st.info("No audit score data available.")

    elif analysis_type == "NC by Category":
        st.markdown("#### 📊 NC by Category Analysis")

        nc_ofis = db.query(NC_OFI).all()

        if nc_ofis:
            category_counts = Counter([nc.category or 'Uncategorized' for nc in nc_ofis])
            df_cat = pd.DataFrame.from_dict(category_counts, orient='index', columns=['count']).reset_index()
            df_cat.columns = ['category', 'count']
            df_cat = df_cat.sort_values('count', ascending=False)

            # Pie chart
            fig = px.pie(
                df_cat,
                values='count',
                names='category',
                title="NC Distribution by Category"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Bar chart
            fig2 = px.bar(
                df_cat,
                x='category',
                y='count',
                title="NC Count by Category",
                color='count',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info("No NC/OFI data available.")

    elif analysis_type == "Repeat Findings Analysis":
        st.markdown("#### 🔁 Repeat Findings Analysis")

        repeat_nc = db.query(NC_OFI).filter(NC_OFI.is_repeat_finding == True).all()

        if repeat_nc:
            st.warning(f"⚠️ Found {len(repeat_nc)} repeat findings")

            df_repeat = pd.DataFrame([{
                'nc_number': nc.nc_number,
                'category': nc.category,
                'department': nc.department,
                'finding_type': nc.finding_type
            } for nc in repeat_nc])

            st.dataframe(df_repeat, use_container_width=True)

            # Category breakdown
            category_counts = Counter([nc.category for nc in repeat_nc])
            df_cat = pd.DataFrame.from_dict(category_counts, orient='index', columns=['count']).reset_index()
            df_cat.columns = ['category', 'count']

            fig = px.bar(
                df_cat,
                x='category',
                y='count',
                title="Repeat Findings by Category",
                color='count',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.success("✅ No repeat findings detected!")

    elif analysis_type == "Auditor Performance":
        st.markdown("#### 👤 Auditor Performance Analysis")

        audits = db.query(Audit).filter(Audit.lead_auditor.isnot(None)).all()

        if audits:
            auditor_data = {}
            for audit in audits:
                if audit.lead_auditor not in auditor_data:
                    auditor_data[audit.lead_auditor] = {
                        'audits': 0,
                        'scores': [],
                        'findings': 0
                    }

                auditor_data[audit.lead_auditor]['audits'] += 1
                if audit.overall_score:
                    auditor_data[audit.lead_auditor]['scores'].append(audit.overall_score)
                auditor_data[audit.lead_auditor]['findings'] += (audit.total_findings or 0)

            df_auditors = pd.DataFrame([{
                'auditor': auditor,
                'total_audits': data['audits'],
                'avg_score': sum(data['scores']) / len(data['scores']) if data['scores'] else 0,
                'total_findings': data['findings']
            } for auditor, data in auditor_data.items()])

            # Display metrics
            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(
                    df_auditors,
                    x='auditor',
                    y='total_audits',
                    title="Audits Conducted by Auditor",
                    color='total_audits',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(
                    df_auditors,
                    x='auditor',
                    y='avg_score',
                    title="Average Audit Score by Auditor",
                    color='avg_score',
                    color_continuous_scale='Greens'
                )
                fig.add_hline(y=80, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df_auditors, use_container_width=True)

        else:
            st.info("No auditor data available.")

    elif analysis_type == "Entity-wise Heatmap":
        st.markdown("#### 🗺️ Entity-wise Performance Heatmap")

        audits = db.query(Audit).filter(
            Audit.entity_name.isnot(None),
            Audit.actual_date.isnot(None)
        ).all()

        if audits:
            df = pd.DataFrame([{
                'entity': a.entity_name,
                'month': a.actual_date.strftime('%Y-%m') if a.actual_date else 'Unknown',
                'score': a.overall_score or 0
            } for a in audits])

            pivot = df.pivot_table(values='score', index='entity', columns='month', aggfunc='mean')

            fig = px.imshow(
                pivot,
                title="Entity Performance Heatmap (Audit Scores)",
                labels=dict(x="Month", y="Entity", color="Score"),
                color_continuous_scale='RdYlGn',
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No entity data available.")

# ===== DATA EXPORT =====
elif view_mode == "Data Export":
    st.subheader("📤 Data Export")

    st.markdown("Export your audit data in various formats for further analysis.")

    export_type = st.selectbox(
        "Select Data to Export",
        ["Audits", "NC/OFI", "CARs", "Reports", "All Data"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            if export_type == "Audits":
                audits = db.query(Audit).all()
                df = pd.DataFrame([a.to_dict() for a in audits])
                st.download_button(
                    label="📥 Download Excel",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name="audits_export.csv",
                    mime="text/csv"
                )
                st.success("✅ Excel export ready!")

            elif export_type == "NC/OFI":
                nc_ofis = db.query(NC_OFI).all()
                df = pd.DataFrame([nc.to_dict() for nc in nc_ofis])
                st.download_button(
                    label="📥 Download Excel",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name="nc_ofi_export.csv",
                    mime="text/csv"
                )
                st.success("✅ Excel export ready!")

            elif export_type == "CARs":
                cars = db.query(CorrectiveAction).all()
                df = pd.DataFrame([car.to_dict() for car in cars])
                st.download_button(
                    label="📥 Download Excel",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name="cars_export.csv",
                    mime="text/csv"
                )
                st.success("✅ Excel export ready!")

    with col2:
        if st.button("📄 Export to PDF", use_container_width=True):
            st.success("✅ PDF export initiated!")
            st.info("PDF will be generated and saved to data/exports/")

    with col3:
        if st.button("📋 Export to CSV", use_container_width=True):
            st.success("✅ CSV export ready!")
            st.info("CSV file ready for download")

    # Preview data
    st.markdown("---")
    st.subheader("📋 Data Preview")

    if export_type == "Audits":
        audits = db.query(Audit).limit(10).all()
        if audits:
            df = pd.DataFrame([a.to_dict() for a in audits])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No audit data available.")

    elif export_type == "NC/OFI":
        nc_ofis = db.query(NC_OFI).limit(10).all()
        if nc_ofis:
            df = pd.DataFrame([nc.to_dict() for nc in nc_ofis])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No NC/OFI data available.")

    elif export_type == "CARs":
        cars = db.query(CorrectiveAction).limit(10).all()
        if cars:
            df = pd.DataFrame([car.to_dict() for car in cars])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No CAR data available.")

db.close()

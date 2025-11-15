"""
Corrective Actions & 8D Methodology Page
"""
import streamlit as st
from datetime import datetime, date, timedelta
from database import get_db
from models.car import CorrectiveAction
from models.nc_ofi import NC_OFI
from models.audit import Audit
import json

st.set_page_config(page_title="Corrective Actions & 8D", page_icon="🔧", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .car-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .discipline-tab {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .progress-indicator {
        background-color: #e9ecef;
        height: 30px;
        border-radius: 15px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    .discipline-complete {
        color: #28a745;
        font-weight: bold;
    }
    .discipline-pending {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
    <div class="car-header">
        <h1>🔧 Corrective Actions & 8D Methodology</h1>
        <p>Systematic Problem Solving and Root Cause Analysis</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.header("🎯 CAR Management")
    action = st.radio(
        "Select Action:",
        ["View CARs", "Create New CAR", "8D Workflow"],
        index=0
    )

    st.markdown("---")
    st.info("""
    **8D Methodology:**
    - D1: Team Formation
    - D2: Problem Description
    - D3: Containment Actions
    - D4: Root Cause Analysis
    - D5: Corrective Actions
    - D6: Implementation
    - D7: Prevention Measures
    - D8: Team Recognition
    """)

# Database session
db = get_db()

# ===== VIEW CARs =====
if action == "View CARs":
    st.subheader("📋 Corrective Action Requests")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Draft", "Submitted", "Approved", "In Progress", "Implemented", "Verified", "Closed"]
        )
    with col2:
        method_filter = st.selectbox(
            "Filter by Method",
            ["All", "8D", "5Why", "Fishbone", "PDCA"]
        )
    with col3:
        search_term = st.text_input("🔍 Search CAR Number")

    # Fetch CARs
    query = db.query(CorrectiveAction)

    if status_filter != "All":
        query = query.filter(CorrectiveAction.status == status_filter)
    if method_filter != "All":
        query = query.filter(CorrectiveAction.method == method_filter)
    if search_term:
        query = query.filter(CorrectiveAction.car_number.contains(search_term))

    cars = query.order_by(CorrectiveAction.created_at.desc()).all()

    if cars:
        st.markdown(f"**Total CARs:** {len(cars)}")

        # Display CARs in cards
        for car in cars:
            with st.expander(f"🔧 {car.car_number} - {car.status} ({car.method})"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"**Status:** {car.status}")
                    st.markdown(f"**Method:** {car.method}")
                    st.markdown(f"**Responsible:** {car.responsible_person or 'Not Assigned'}")

                with col2:
                    st.markdown(f"**Due Date:** {car.due_date or 'Not Set'}")
                    st.markdown(f"**Created:** {car.created_at.strftime('%Y-%m-%d') if car.created_at else 'N/A'}")
                    if car.method == "8D":
                        progress = car.get_8d_progress()
                        st.markdown(f"**8D Progress:** {progress:.0f}%")

                with col3:
                    st.markdown(f"**Verified:** {'✅ Yes' if car.effectiveness_verified else '❌ No'}")
                    if car.completion_date:
                        st.markdown(f"**Completed:** {car.completion_date}")

                # Progress bar for 8D
                if car.method == "8D":
                    progress = car.get_8d_progress()
                    st.markdown(f"""
                        <div class="progress-indicator">
                            <div class="progress-bar" style="width: {progress}%"></div>
                        </div>
                    """, unsafe_allow_html=True)

                # Action buttons
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    if st.button(f"Edit", key=f"edit_{car.id}"):
                        st.session_state['edit_car_id'] = car.id
                        st.rerun()
                with col2:
                    if st.button(f"Delete", key=f"delete_{car.id}"):
                        db.delete(car)
                        db.commit()
                        st.success(f"CAR {car.car_number} deleted!")
                        st.rerun()
    else:
        st.info("No CARs found. Create a new CAR to get started!")

# ===== CREATE NEW CAR =====
elif action == "Create New CAR":
    st.subheader("➕ Create New Corrective Action Request")

    with st.form("new_car_form"):
        st.markdown("### Basic Information")

        col1, col2 = st.columns(2)

        with col1:
            # Fetch available NC/OFI
            nc_ofis = db.query(NC_OFI).filter(NC_OFI.status.in_(['Open', 'CAR Initiated'])).all()

            if nc_ofis:
                nc_options = {f"{nc.nc_number} - {nc.finding_type}": nc.id for nc in nc_ofis}
                selected_nc = st.selectbox("Select NC/OFI *", options=list(nc_options.keys()))
                nc_ofi_id = nc_options[selected_nc]
            else:
                st.warning("⚠️ No open NC/OFI found. Please create an NC/OFI first.")
                nc_ofi_id = None

            method = st.selectbox(
                "CAR Method *",
                ["8D", "5Why", "Fishbone", "PDCA"],
                index=0
            )

            responsible_person = st.text_input("Responsible Person *", placeholder="John Doe")

        with col2:
            car_number = st.text_input(
                "CAR Number *",
                value=f"CAR-{datetime.now().strftime('%Y%m%d')}-{db.query(CorrectiveAction).count() + 1:03d}"
            )

            due_date = st.date_input(
                "Due Date *",
                value=date.today() + timedelta(days=30)
            )

            status = st.selectbox(
                "Status",
                ["Draft", "Submitted", "Approved"],
                index=0
            )

        st.markdown("### Initial Actions")

        immediate_action = st.text_area(
            "Immediate Action Taken",
            placeholder="Describe any immediate containment actions...",
            height=100
        )

        submit = st.form_submit_button("🚀 Create CAR", use_container_width=True)

        if submit:
            if not nc_ofi_id:
                st.error("Please select an NC/OFI!")
            elif not responsible_person:
                st.error("Please enter a responsible person!")
            else:
                try:
                    new_car = CorrectiveAction(
                        car_number=car_number,
                        nc_ofi_id=nc_ofi_id,
                        method=method,
                        responsible_person=responsible_person,
                        due_date=due_date,
                        status=status,
                        immediate_action=immediate_action,
                        created_by="Current User",
                        created_at=datetime.utcnow()
                    )

                    db.add(new_car)
                    db.commit()

                    st.success(f"✅ CAR {car_number} created successfully!")
                    st.balloons()

                    # Update NC/OFI status
                    nc_ofi = db.query(NC_OFI).filter(NC_OFI.id == nc_ofi_id).first()
                    if nc_ofi:
                        nc_ofi.status = "CAR Initiated"
                        nc_ofi.requires_car = True
                        db.commit()

                    st.info("Navigate to '8D Workflow' to complete the 8D disciplines.")

                except Exception as e:
                    st.error(f"Error creating CAR: {e}")
                    db.rollback()

# ===== 8D WORKFLOW =====
elif action == "8D Workflow":
    st.subheader("📊 8D Problem Solving Workflow")

    # Select CAR
    cars_8d = db.query(CorrectiveAction).filter(CorrectiveAction.method == "8D").all()

    if not cars_8d:
        st.warning("⚠️ No CARs using 8D methodology found. Please create a CAR with 8D method first.")
    else:
        car_options = {f"{car.car_number} - {car.status}": car.id for car in cars_8d}
        selected_car = st.selectbox("Select CAR for 8D Workflow", options=list(car_options.keys()))

        car_id = car_options[selected_car]
        car = db.query(CorrectiveAction).filter(CorrectiveAction.id == car_id).first()

        if car:
            # Display progress
            progress = car.get_8d_progress()
            st.markdown(f"**Overall Progress:** {progress:.0f}%")
            st.markdown(f"""
                <div class="progress-indicator">
                    <div class="progress-bar" style="width: {progress}%"></div>
                </div>
            """, unsafe_allow_html=True)

            # 8D Tabs
            tabs = st.tabs([
                "D1: Team",
                "D2: Problem",
                "D3: Containment",
                "D4: Root Cause",
                "D5: Actions",
                "D6: Implementation",
                "D7: Prevention",
                "D8: Recognition"
            ])

            # === D1: TEAM FORMATION ===
            with tabs[0]:
                st.markdown("### D1: Team Formation")
                st.markdown("Form a cross-functional team with knowledge of the process/product.")

                with st.form("d1_form"):
                    col1, col2 = st.columns(2)

                    with col1:
                        d1_team_leader = st.text_input(
                            "Team Leader *",
                            value=car.d1_team_leader or ""
                        )

                        d1_team_members = st.text_area(
                            "Team Members (one per line)",
                            value=car.d1_team_members or "",
                            height=150,
                            placeholder="Name - Role - Department\nJohn Doe - Quality Engineer - QA\nJane Smith - Production Lead - Manufacturing"
                        )

                    with col2:
                        d1_completion_date = st.date_input(
                            "Completion Date",
                            value=car.d1_completion_date or date.today()
                        )

                        d1_notes = st.text_area(
                            "Notes",
                            value=car.d1_notes or "",
                            height=150
                        )

                    if st.form_submit_button("💾 Save D1", use_container_width=True):
                        car.d1_team_leader = d1_team_leader
                        car.d1_team_members = d1_team_members
                        car.d1_completion_date = d1_completion_date
                        car.d1_notes = d1_notes
                        db.commit()
                        st.success("✅ D1: Team Formation saved!")
                        st.rerun()

            # === D2: PROBLEM DESCRIPTION (5W2H) ===
            with tabs[1]:
                st.markdown("### D2: Problem Description (5W2H)")
                st.markdown("Describe the problem using the 5W2H method.")

                with st.form("d2_form"):
                    d2_what = st.text_area("What is the problem?", value=car.d2_what or "", height=100)
                    d2_when = st.text_area("When did it occur?", value=car.d2_when or "", height=80)

                    col1, col2 = st.columns(2)
                    with col1:
                        d2_where = st.text_area("Where did it occur?", value=car.d2_where or "", height=80)
                        d2_who = st.text_area("Who discovered it?", value=car.d2_who or "", height=80)
                    with col2:
                        d2_why = st.text_area("Why is it a problem?", value=car.d2_why or "", height=80)
                        d2_how = st.text_area("How was it detected?", value=car.d2_how or "", height=80)

                    d2_how_many = st.text_area("How many are affected?", value=car.d2_how_many or "", height=80)

                    d2_completion_date = st.date_input("Completion Date", value=car.d2_completion_date or date.today())
                    d2_notes = st.text_area("Additional Notes", value=car.d2_notes or "", height=100)

                    if st.form_submit_button("💾 Save D2", use_container_width=True):
                        car.d2_what = d2_what
                        car.d2_when = d2_when
                        car.d2_where = d2_where
                        car.d2_who = d2_who
                        car.d2_why = d2_why
                        car.d2_how = d2_how
                        car.d2_how_many = d2_how_many
                        car.d2_completion_date = d2_completion_date
                        car.d2_notes = d2_notes
                        db.commit()
                        st.success("✅ D2: Problem Description saved!")
                        st.rerun()

            # === D3: CONTAINMENT ACTIONS ===
            with tabs[2]:
                st.markdown("### D3: Interim Containment Actions")
                st.markdown("Implement immediate actions to isolate the problem from customers.")

                with st.form("d3_form"):
                    d3_immediate_actions = st.text_area(
                        "Immediate Containment Actions",
                        value=car.d3_immediate_actions or "",
                        height=150,
                        placeholder="1. Quarantine affected products\n2. Inspect all inventory\n3. Increase inspection frequency"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        d3_containment_verified = st.checkbox(
                            "Containment Verified Effective",
                            value=car.d3_containment_verified or False
                        )
                    with col2:
                        d3_completion_date = st.date_input(
                            "Completion Date",
                            value=car.d3_completion_date or date.today()
                        )

                    d3_effectiveness = st.text_area(
                        "Effectiveness Evidence",
                        value=car.d3_effectiveness or "",
                        height=100
                    )

                    d3_notes = st.text_area("Notes", value=car.d3_notes or "", height=100)

                    if st.form_submit_button("💾 Save D3", use_container_width=True):
                        car.d3_immediate_actions = d3_immediate_actions
                        car.d3_containment_verified = d3_containment_verified
                        car.d3_effectiveness = d3_effectiveness
                        car.d3_completion_date = d3_completion_date
                        car.d3_notes = d3_notes
                        db.commit()
                        st.success("✅ D3: Containment Actions saved!")
                        st.rerun()

            # === D4: ROOT CAUSE ANALYSIS ===
            with tabs[3]:
                st.markdown("### D4: Root Cause Analysis")
                st.markdown("Identify and verify the root cause using analytical tools.")

                analysis_method = st.radio(
                    "Select Analysis Method",
                    ["5-Why Analysis", "Fishbone Diagram", "Other"],
                    horizontal=True
                )

                if analysis_method == "5-Why Analysis":
                    with st.form("d4_5why_form"):
                        st.markdown("#### 5-Why Analysis")

                        d4_why1 = st.text_area("Why 1?", value=car.d4_why1 or "", height=80)
                        d4_why2 = st.text_area("Why 2?", value=car.d4_why2 or "", height=80)
                        d4_why3 = st.text_area("Why 3?", value=car.d4_why3 or "", height=80)
                        d4_why4 = st.text_area("Why 4?", value=car.d4_why4 or "", height=80)
                        d4_why5 = st.text_area("Why 5? (Root Cause)", value=car.d4_why5 or "", height=80)

                        d4_root_cause_verified = st.checkbox("Root Cause Verified", value=car.d4_root_cause_verified or False)
                        d4_completion_date = st.date_input("Completion Date", value=car.d4_completion_date or date.today())
                        d4_notes = st.text_area("Notes", value=car.d4_notes or "", height=100)

                        if st.form_submit_button("💾 Save D4", use_container_width=True):
                            car.d4_analysis_method = "5-Why"
                            car.d4_why1 = d4_why1
                            car.d4_why2 = d4_why2
                            car.d4_why3 = d4_why3
                            car.d4_why4 = d4_why4
                            car.d4_why5 = d4_why5
                            car.d4_root_cause = d4_why5  # Root cause is the final Why
                            car.d4_root_cause_verified = d4_root_cause_verified
                            car.d4_completion_date = d4_completion_date
                            car.d4_notes = d4_notes
                            db.commit()
                            st.success("✅ D4: Root Cause Analysis saved!")
                            st.rerun()

                elif analysis_method == "Fishbone Diagram":
                    with st.form("d4_fishbone_form"):
                        st.markdown("#### Fishbone Diagram (Ishikawa)")
                        st.info("Enter potential causes for each category")

                        col1, col2 = st.columns(2)
                        with col1:
                            man = st.text_area("Man (People)", height=80)
                            method = st.text_area("Method (Process)", height=80)
                            machine = st.text_area("Machine (Equipment)", height=80)
                        with col2:
                            material = st.text_area("Material", height=80)
                            measurement = st.text_area("Measurement", height=80)
                            environment = st.text_area("Environment", height=80)

                        d4_root_cause = st.text_area("Identified Root Cause", height=100)
                        d4_root_cause_verified = st.checkbox("Root Cause Verified", value=False)
                        d4_completion_date = st.date_input("Completion Date", value=date.today())

                        if st.form_submit_button("💾 Save D4", use_container_width=True):
                            fishbone_data = {
                                "man": man,
                                "method": method,
                                "machine": machine,
                                "material": material,
                                "measurement": measurement,
                                "environment": environment
                            }
                            car.d4_analysis_method = "Fishbone"
                            car.d4_fishbone_data = json.dumps(fishbone_data)
                            car.d4_root_cause = d4_root_cause
                            car.d4_root_cause_verified = d4_root_cause_verified
                            car.d4_completion_date = d4_completion_date
                            db.commit()
                            st.success("✅ D4: Root Cause Analysis saved!")
                            st.rerun()

            # === D5: PERMANENT CORRECTIVE ACTIONS ===
            with tabs[4]:
                st.markdown("### D5: Permanent Corrective Actions")
                st.markdown("Choose and verify permanent corrective actions.")

                with st.form("d5_form"):
                    d5_corrective_actions = st.text_area(
                        "Corrective Actions",
                        value=car.d5_corrective_actions or "",
                        height=150,
                        placeholder="1. Update process documentation\n2. Implement poka-yoke device\n3. Revise training program"
                    )

                    d5_why_selected = st.text_area(
                        "Why These Actions Were Selected",
                        value=car.d5_why_selected or "",
                        height=100
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        d5_completion_date = st.date_input("Completion Date", value=car.d5_completion_date or date.today())
                    with col2:
                        d5_notes = st.text_area("Notes", value=car.d5_notes or "", height=100)

                    if st.form_submit_button("💾 Save D5", use_container_width=True):
                        car.d5_corrective_actions = d5_corrective_actions
                        car.d5_why_selected = d5_why_selected
                        car.d5_completion_date = d5_completion_date
                        car.d5_notes = d5_notes
                        car.permanent_action = d5_corrective_actions  # Update main field
                        db.commit()
                        st.success("✅ D5: Corrective Actions saved!")
                        st.rerun()

            # === D6: IMPLEMENTATION ===
            with tabs[5]:
                st.markdown("### D6: Implementation")
                st.markdown("Implement the permanent corrective actions.")

                with st.form("d6_form"):
                    d6_implementation_plan = st.text_area(
                        "Implementation Plan",
                        value=car.d6_implementation_plan or "",
                        height=150
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        d6_resources_required = st.text_area(
                            "Resources Required",
                            value=car.d6_resources_required or "",
                            height=100
                        )
                        d6_training_required = st.text_area(
                            "Training Required",
                            value=car.d6_training_required or "",
                            height=100
                        )
                    with col2:
                        d6_timeline = st.text_area(
                            "Timeline",
                            value=car.d6_timeline or "",
                            height=100
                        )
                        d6_completion_date = st.date_input("Completion Date", value=car.d6_completion_date or date.today())

                    d6_notes = st.text_area("Notes", value=car.d6_notes or "", height=100)

                    if st.form_submit_button("💾 Save D6", use_container_width=True):
                        car.d6_implementation_plan = d6_implementation_plan
                        car.d6_resources_required = d6_resources_required
                        car.d6_training_required = d6_training_required
                        car.d6_timeline = d6_timeline
                        car.d6_completion_date = d6_completion_date
                        car.d6_notes = d6_notes
                        db.commit()
                        st.success("✅ D6: Implementation saved!")
                        st.rerun()

            # === D7: PREVENTION ===
            with tabs[6]:
                st.markdown("### D7: Prevent Recurrence")
                st.markdown("Modify systems and processes to prevent recurrence.")

                with st.form("d7_form"):
                    d7_process_changes = st.text_area(
                        "Process Changes",
                        value=car.d7_process_changes or "",
                        height=100
                    )

                    d7_system_improvements = st.text_area(
                        "System Improvements",
                        value=car.d7_system_improvements or "",
                        height=100
                    )

                    d7_documentation_updates = st.text_area(
                        "Documentation Updates",
                        value=car.d7_documentation_updates or "",
                        height=100
                    )

                    d7_training_plan = st.text_area(
                        "Training Plan",
                        value=car.d7_training_plan or "",
                        height=100
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        d7_completion_date = st.date_input("Completion Date", value=car.d7_completion_date or date.today())
                    with col2:
                        d7_notes = st.text_area("Notes", value=car.d7_notes or "", height=100)

                    if st.form_submit_button("💾 Save D7", use_container_width=True):
                        car.d7_process_changes = d7_process_changes
                        car.d7_system_improvements = d7_system_improvements
                        car.d7_documentation_updates = d7_documentation_updates
                        car.d7_training_plan = d7_training_plan
                        car.d7_completion_date = d7_completion_date
                        car.d7_notes = d7_notes
                        db.commit()
                        st.success("✅ D7: Prevention saved!")
                        st.rerun()

            # === D8: TEAM RECOGNITION ===
            with tabs[7]:
                st.markdown("### D8: Congratulate the Team")
                st.markdown("Recognize team contributions and document lessons learned.")

                with st.form("d8_form"):
                    d8_team_contributions = st.text_area(
                        "Team Contributions",
                        value=car.d8_team_contributions or "",
                        height=120,
                        placeholder="Recognize individual and team achievements..."
                    )

                    d8_lessons_learned = st.text_area(
                        "Lessons Learned",
                        value=car.d8_lessons_learned or "",
                        height=120,
                        placeholder="What did we learn from this problem?"
                    )

                    d8_best_practices = st.text_area(
                        "Best Practices",
                        value=car.d8_best_practices or "",
                        height=120,
                        placeholder="What best practices should be shared?"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        d8_recognition_method = st.text_input(
                            "Recognition Method",
                            value=car.d8_recognition_method or "",
                            placeholder="e.g., Team lunch, Certificate, Award"
                        )
                    with col2:
                        d8_completion_date = st.date_input("Completion Date", value=car.d8_completion_date or date.today())

                    d8_notes = st.text_area("Notes", value=car.d8_notes or "", height=100)

                    if st.form_submit_button("💾 Save D8 & Complete", use_container_width=True):
                        car.d8_team_contributions = d8_team_contributions
                        car.d8_lessons_learned = d8_lessons_learned
                        car.d8_best_practices = d8_best_practices
                        car.d8_recognition_method = d8_recognition_method
                        car.d8_completion_date = d8_completion_date
                        car.d8_notes = d8_notes

                        # If all disciplines complete, update status
                        if car.get_8d_progress() == 100:
                            car.status = "Implemented"

                        db.commit()
                        st.success("✅ D8: Team Recognition saved!")
                        st.balloons()
                        st.rerun()

db.close()

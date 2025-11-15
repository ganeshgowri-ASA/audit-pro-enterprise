"""
Entity Management Page

Hierarchical organization structure management with:
- Tree view of entities
- Add/Edit/Deactivate operations
- Search and filter
- Excel export
"""
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

from database.session import get_db
from models.entity import Entity
from utils.entity_helpers import (
    validate_circular_reference,
    calculate_entity_level,
    get_entity_type_for_level,
    build_entity_tree,
    get_parent_candidates,
    search_entities,
    export_entities_to_dict,
    get_entity_statistics
)
from config.settings import ENTITY_TYPES, MAX_HIERARCHY_LEVEL

# Page configuration
st.set_page_config(
    page_title="Entity Management - Audit Pro Enterprise",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Entity Hierarchy Management")
st.markdown("Manage organizational structure with hierarchical entities")

# Initialize session state
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False
if 'edit_entity_id' not in st.session_state:
    st.session_state.edit_entity_id = None
if 'view_entity_id' not in st.session_state:
    st.session_state.view_entity_id = None


def reset_forms():
    """Reset all form states"""
    st.session_state.show_add_form = False
    st.session_state.edit_entity_id = None
    st.session_state.view_entity_id = None


def render_entity_tree(entities, level=0):
    """Recursively render entity tree with expandable sections"""
    for entity in entities:
        # Create expander for each entity
        icon = "🏢" if entity['level'] == 0 else "🏭" if entity['level'] == 1 else "⚙️" if entity['level'] == 2 else "🔧" if entity['level'] == 3 else "📦"

        with st.expander(f"{icon} {entity['name']} ({entity['type']})", expanded=level < 1):
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

            with col1:
                st.write(f"**Level:** {entity['level']} | **Type:** {entity['type']}")
                if entity['location']:
                    st.write(f"📍 {entity['location']}")

            with col2:
                if entity['contact_person']:
                    st.write(f"👤 {entity['contact_person']}")
                if entity['email']:
                    st.write(f"✉️ {entity['email']}")

            with col3:
                if st.button("👁️ View", key=f"view_{entity['id']}"):
                    st.session_state.view_entity_id = entity['id']
                    st.rerun()

            with col4:
                if st.button("✏️ Edit", key=f"edit_{entity['id']}"):
                    st.session_state.edit_entity_id = entity['id']
                    st.rerun()

            # Render children recursively
            if entity['children']:
                render_entity_tree(entity['children'], level + 1)


def render_add_entity_form():
    """Render form to add new entity"""
    st.subheader("➕ Add New Entity")

    with st.form("add_entity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Entity Name *", placeholder="e.g., Plant A")

            level = st.selectbox(
                "Hierarchy Level *",
                options=list(ENTITY_TYPES.keys()),
                format_func=lambda x: f"Level {x} - {ENTITY_TYPES[x]}"
            )

            entity_type = ENTITY_TYPES[level]
            st.info(f"Type: **{entity_type}**")

            # Get parent candidates
            with get_db() as db:
                parent_options = get_parent_candidates(db, None, level)

            parent_id = None
            if level > 0:
                if parent_options:
                    parent_display = st.selectbox(
                        f"Parent Entity * (Must be Level {level - 1})",
                        options=[None] + parent_options,
                        format_func=lambda x: "-- Select Parent --" if x is None else x[0]
                    )
                    if parent_display:
                        parent_id = parent_display[1]
                else:
                    st.error(f"No parent entities available at Level {level - 1}. Please create a Level {level - 1} entity first.")

            location = st.text_input("Location", placeholder="e.g., Mumbai, India")

        with col2:
            contact_person = st.text_input("Contact Person", placeholder="e.g., John Doe")
            email = st.text_input("Email", placeholder="e.g., john.doe@example.com")
            phone = st.text_input("Phone", placeholder="e.g., +91-1234567890")
            is_active = st.checkbox("Active", value=True)

        address = st.text_area("Address", placeholder="Full address...")
        description = st.text_area("Description", placeholder="Optional description...")

        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            submitted = st.form_submit_button("💾 Save Entity", use_container_width=True)
        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                reset_forms()
                st.rerun()

        if submitted:
            # Validation
            if not name:
                st.error("Entity name is required")
            elif level > 0 and not parent_id:
                st.error(f"Parent entity is required for Level {level}")
            else:
                try:
                    with get_db() as db:
                        # Validate circular reference
                        is_valid, error_msg = validate_circular_reference(db, None, parent_id)
                        if not is_valid:
                            st.error(error_msg)
                        else:
                            # Create entity
                            new_entity = Entity(
                                name=name,
                                type=entity_type,
                                parent_id=parent_id,
                                level=level,
                                location=location,
                                address=address,
                                contact_person=contact_person,
                                email=email,
                                phone=phone,
                                is_active=is_active,
                                description=description
                            )
                            db.add(new_entity)
                            db.commit()
                            st.success(f"✅ Entity '{name}' created successfully!")
                            reset_forms()
                            st.rerun()
                except Exception as e:
                    st.error(f"Error creating entity: {str(e)}")


def render_edit_entity_form(entity_id):
    """Render form to edit existing entity"""
    with get_db() as db:
        entity = db.query(Entity).filter(Entity.id == entity_id).first()

        if not entity:
            st.error("Entity not found")
            reset_forms()
            return

        st.subheader(f"✏️ Edit Entity: {entity.name}")

        with st.form("edit_entity_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Entity Name *", value=entity.name)

                st.info(f"**Level:** {entity.level} - {entity.type}")

                # Get parent candidates
                parent_options = get_parent_candidates(db, entity.id, entity.level)

                parent_id = entity.parent_id
                if entity.level > 0:
                    if parent_options:
                        current_parent_idx = 0
                        if entity.parent_id:
                            for idx, (_, pid) in enumerate(parent_options):
                                if pid == entity.parent_id:
                                    current_parent_idx = idx
                                    break

                        parent_display = st.selectbox(
                            f"Parent Entity (Level {entity.level - 1})",
                            options=parent_options,
                            index=current_parent_idx,
                            format_func=lambda x: x[0]
                        )
                        parent_id = parent_display[1]

                location = st.text_input("Location", value=entity.location or "")

            with col2:
                contact_person = st.text_input("Contact Person", value=entity.contact_person or "")
                email = st.text_input("Email", value=entity.email or "")
                phone = st.text_input("Phone", value=entity.phone or "")
                is_active = st.checkbox("Active", value=entity.is_active)

            address = st.text_area("Address", value=entity.address or "")
            description = st.text_area("Description", value=entity.description or "")

            col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
            with col1:
                submitted = st.form_submit_button("💾 Update", use_container_width=True)
            with col2:
                deactivate = st.form_submit_button("🚫 Deactivate", use_container_width=True)
            with col3:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    reset_forms()
                    st.rerun()

            if submitted:
                if not name:
                    st.error("Entity name is required")
                else:
                    try:
                        # Validate circular reference
                        is_valid, error_msg = validate_circular_reference(db, entity_id, parent_id)
                        if not is_valid:
                            st.error(error_msg)
                        else:
                            # Update entity
                            entity.name = name
                            entity.parent_id = parent_id
                            entity.location = location
                            entity.address = address
                            entity.contact_person = contact_person
                            entity.email = email
                            entity.phone = phone
                            entity.is_active = is_active
                            entity.description = description
                            entity.updated_at = datetime.utcnow()

                            db.commit()
                            st.success(f"✅ Entity '{name}' updated successfully!")
                            reset_forms()
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error updating entity: {str(e)}")

            if deactivate:
                entity.is_active = False
                entity.updated_at = datetime.utcnow()
                db.commit()
                st.success(f"Entity '{entity.name}' deactivated")
                reset_forms()
                st.rerun()


def render_entity_details(entity_id):
    """Render detailed view of entity"""
    with get_db() as db:
        entity = db.query(Entity).filter(Entity.id == entity_id).first()

        if not entity:
            st.error("Entity not found")
            reset_forms()
            return

        st.subheader(f"👁️ Entity Details: {entity.name}")

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.markdown("### Basic Information")
            st.write(f"**ID:** {entity.id}")
            st.write(f"**Name:** {entity.name}")
            st.write(f"**Type:** {entity.type}")
            st.write(f"**Level:** {entity.level}")
            st.write(f"**Status:** {'✅ Active' if entity.is_active else '❌ Inactive'}")
            st.write(f"**Full Path:** {entity.get_full_path()}")

        with col2:
            st.markdown("### Contact Information")
            st.write(f"**Location:** {entity.location or 'N/A'}")
            st.write(f"**Contact Person:** {entity.contact_person or 'N/A'}")
            st.write(f"**Email:** {entity.email or 'N/A'}")
            st.write(f"**Phone:** {entity.phone or 'N/A'}")

        with col3:
            if st.button("✏️ Edit", use_container_width=True):
                st.session_state.edit_entity_id = entity_id
                st.session_state.view_entity_id = None
                st.rerun()
            if st.button("❌ Close", use_container_width=True):
                reset_forms()
                st.rerun()

        if entity.address:
            st.markdown("### Address")
            st.write(entity.address)

        if entity.description:
            st.markdown("### Description")
            st.write(entity.description)

        st.markdown("### Hierarchy Information")
        col1, col2 = st.columns(2)

        with col1:
            if entity.parent:
                st.write(f"**Parent:** {entity.parent.name} ({entity.parent.type})")
            else:
                st.write("**Parent:** Root Entity")

            st.write(f"**Can Have Children:** {'Yes' if entity.can_have_children() else 'No'}")
            if entity.can_have_children():
                st.write(f"**Expected Child Type:** {entity.get_expected_child_type()}")

        with col2:
            children = entity.children
            st.write(f"**Direct Children:** {len(children)}")
            all_children = entity.get_all_children()
            st.write(f"**Total Descendants:** {len(all_children)}")

        if children:
            st.markdown("### Direct Children")
            for child in children:
                st.write(f"- {child.name} ({child.type}) - {'✅ Active' if child.is_active else '❌ Inactive'}")

        st.markdown("### Metadata")
        st.write(f"**Created:** {entity.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Last Updated:** {entity.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")


# Main layout
# Sidebar - Statistics and Filters
with st.sidebar:
    st.header("📊 Statistics")

    with get_db() as db:
        stats = get_entity_statistics(db)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Entities", stats['total'])
        st.metric("Active", stats['active'])
    with col2:
        st.metric("Inactive", stats['inactive'])

    st.markdown("### By Type")
    for entity_type, count in stats['by_type'].items():
        st.write(f"**{entity_type}:** {count}")

    st.divider()

    st.header("🔍 Search & Filter")

    search_term = st.text_input("Search", placeholder="Entity name, location, contact...")

    filter_type = st.selectbox(
        "Filter by Type",
        options=["All"] + list(ENTITY_TYPES.values())
    )

    filter_level = st.selectbox(
        "Filter by Level",
        options=["All"] + [f"Level {i}" for i in range(MAX_HIERARCHY_LEVEL + 1)]
    )

    show_inactive = st.checkbox("Show Inactive", value=False)

    st.divider()

    # Export to Excel
    st.header("📥 Export")
    if st.button("📊 Export to Excel", use_container_width=True):
        with get_db() as db:
            export_data = export_entities_to_dict(db, active_only=not show_inactive)

        df = pd.DataFrame(export_data)

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Entities')

        excel_data = output.getvalue()

        st.download_button(
            label="💾 Download Excel",
            data=excel_data,
            file_name=f"entities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# Main content area
# Action buttons
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("➕ Add Entity", use_container_width=True):
        st.session_state.show_add_form = not st.session_state.show_add_form
        st.session_state.edit_entity_id = None
        st.session_state.view_entity_id = None
        st.rerun()

with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        reset_forms()
        st.rerun()

st.divider()

# Show forms based on state
if st.session_state.show_add_form:
    render_add_entity_form()
    st.divider()

if st.session_state.edit_entity_id:
    render_edit_entity_form(st.session_state.edit_entity_id)
    st.divider()

if st.session_state.view_entity_id:
    render_entity_details(st.session_state.view_entity_id)
    st.divider()

# Display entity tree
st.subheader("🌳 Entity Hierarchy Tree")

with get_db() as db:
    # Apply filters
    if search_term:
        filter_type_value = None if filter_type == "All" else filter_type
        filter_level_value = None if filter_level == "All" else int(filter_level.split()[-1])

        entities = search_entities(
            db,
            search_term,
            entity_type=filter_type_value,
            level=filter_level_value,
            active_only=not show_inactive
        )

        st.info(f"Found {len(entities)} matching entities")

        if entities:
            for entity in entities:
                with st.expander(f"🔍 {entity.name} ({entity.type}) - Level {entity.level}"):
                    col1, col2, col3 = st.columns([2, 2, 1])

                    with col1:
                        st.write(f"**Full Path:** {entity.get_full_path()}")
                        st.write(f"**Location:** {entity.location or 'N/A'}")

                    with col2:
                        st.write(f"**Contact:** {entity.contact_person or 'N/A'}")
                        st.write(f"**Email:** {entity.email or 'N/A'}")

                    with col3:
                        if st.button("👁️ View", key=f"search_view_{entity.id}"):
                            st.session_state.view_entity_id = entity.id
                            st.rerun()
    else:
        # Build and display tree
        entity_tree = build_entity_tree(db, active_only=not show_inactive)

        if entity_tree:
            render_entity_tree(entity_tree)
        else:
            st.info("No entities found. Click 'Add Entity' to create your first organizational unit.")

# Footer
st.divider()
st.caption("🏢 Entity Hierarchy Management - Audit Pro Enterprise v1.0.0")

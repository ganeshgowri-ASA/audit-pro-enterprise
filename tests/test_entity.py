"""
Comprehensive tests for Entity model and hierarchy management

Tests:
- test_hierarchy_integrity()
- test_circular_reference_prevention()
- test_entity_crud()
"""
import pytest
from sqlalchemy.exc import IntegrityError
from models.entity import Entity
from utils.entity_helpers import (
    validate_circular_reference,
    calculate_entity_level,
    build_entity_tree,
    search_entities
)
from config.settings import ENTITY_TYPES


class TestEntityCRUD:
    """Test basic CRUD operations for Entity"""

    def test_create_entity(self, db_session):
        """Test creating a new entity"""
        entity = Entity(
            name="Test Entity",
            type="Corporate",
            level=0,
            parent_id=None,
            location="Test Location",
            is_active=True
        )
        db_session.add(entity)
        db_session.commit()

        assert entity.id is not None
        assert entity.name == "Test Entity"
        assert entity.type == "Corporate"
        assert entity.level == 0
        assert entity.is_active is True

    def test_read_entity(self, db_session, sample_entities):
        """Test reading an entity"""
        corporate = sample_entities["corporate"]

        fetched = db_session.query(Entity).filter(Entity.id == corporate.id).first()

        assert fetched is not None
        assert fetched.name == "Test Corp"
        assert fetched.type == "Corporate"

    def test_update_entity(self, db_session, sample_entities):
        """Test updating an entity"""
        plant_a = sample_entities["plant_a"]

        plant_a.name = "Plant A Updated"
        plant_a.location = "New Location"
        db_session.commit()

        fetched = db_session.query(Entity).filter(Entity.id == plant_a.id).first()
        assert fetched.name == "Plant A Updated"
        assert fetched.location == "New Location"

    def test_delete_entity(self, db_session):
        """Test deleting an entity (soft delete via is_active)"""
        entity = Entity(
            name="To Delete",
            type="Corporate",
            level=0,
            is_active=True
        )
        db_session.add(entity)
        db_session.commit()

        entity_id = entity.id

        # Soft delete
        entity.is_active = False
        db_session.commit()

        fetched = db_session.query(Entity).filter(Entity.id == entity_id).first()
        assert fetched is not None
        assert fetched.is_active is False

    def test_entity_with_all_fields(self, db_session):
        """Test creating entity with all fields populated"""
        entity = Entity(
            name="Complete Entity",
            type="Plant",
            level=1,
            parent_id=None,
            location="Mumbai",
            address="123 Test Street",
            contact_person="John Doe",
            email="john@test.com",
            phone="+91-1234567890",
            is_active=True,
            description="Test description"
        )
        db_session.add(entity)
        db_session.commit()

        assert entity.id is not None
        assert entity.contact_person == "John Doe"
        assert entity.email == "john@test.com"
        assert entity.phone == "+91-1234567890"
        assert entity.description == "Test description"


class TestHierarchyIntegrity:
    """Test hierarchy integrity and relationships"""

    def test_parent_child_relationship(self, db_session, sample_entities):
        """Test parent-child relationships are correctly established"""
        corporate = sample_entities["corporate"]
        plant_a = sample_entities["plant_a"]

        assert plant_a.parent_id == corporate.id
        assert plant_a.parent == corporate
        assert plant_a in corporate.children

    def test_hierarchy_levels(self, db_session, sample_entities):
        """Test hierarchy levels are correctly set"""
        corporate = sample_entities["corporate"]
        plant_a = sample_entities["plant_a"]
        line_1 = sample_entities["line_1"]
        process_1 = sample_entities["process_1"]

        assert corporate.level == 0
        assert plant_a.level == 1
        assert line_1.level == 2
        assert process_1.level == 3

    def test_get_full_path(self, db_session, sample_entities):
        """Test getting full hierarchical path"""
        process_1 = sample_entities["process_1"]

        full_path = process_1.get_full_path()
        expected_path = "Test Corp > Plant A > Line 1 > Process 1"

        assert full_path == expected_path

    def test_get_full_path_custom_separator(self, db_session, sample_entities):
        """Test getting full path with custom separator"""
        line_1 = sample_entities["line_1"]

        full_path = line_1.get_full_path(separator=" / ")
        expected_path = "Test Corp / Plant A / Line 1"

        assert full_path == expected_path

    def test_get_all_children(self, db_session, sample_entities):
        """Test getting all descendants"""
        corporate = sample_entities["corporate"]

        all_children = corporate.get_all_children()

        # Should have 5 descendants: 2 plants, 2 lines, 1 process
        assert len(all_children) == 5

        names = [child.name for child in all_children]
        assert "Plant A" in names
        assert "Plant B" in names
        assert "Line 1" in names
        assert "Line 2" in names
        assert "Process 1" in names

    def test_get_ancestors(self, db_session, sample_entities):
        """Test getting all ancestors"""
        process_1 = sample_entities["process_1"]

        ancestors = process_1.get_ancestors()

        assert len(ancestors) == 3
        assert ancestors[0].name == "Line 1"  # Direct parent
        assert ancestors[1].name == "Plant A"
        assert ancestors[2].name == "Test Corp"  # Root

    def test_can_have_children(self, db_session, sample_entities):
        """Test checking if entity can have children"""
        corporate = sample_entities["corporate"]
        process_1 = sample_entities["process_1"]

        assert corporate.can_have_children() is True  # Level 0 can have children

        # Add a Level 4 entity (Sub-Process)
        sub_process = Entity(
            name="Sub Process",
            type="Sub-Process",
            level=4,
            parent_id=process_1.id,
            is_active=True
        )
        db_session.add(sub_process)
        db_session.commit()

        assert sub_process.can_have_children() is False  # Level 4 is max

    def test_get_expected_child_type(self, db_session, sample_entities):
        """Test getting expected child type"""
        corporate = sample_entities["corporate"]
        plant_a = sample_entities["plant_a"]
        line_1 = sample_entities["line_1"]

        assert corporate.get_expected_child_type() == "Plant"
        assert plant_a.get_expected_child_type() == "Line"
        assert line_1.get_expected_child_type() == "Process"

    def test_root_entity_no_parent(self, db_session):
        """Test that root entity (level 0) has no parent"""
        corporate = Entity(
            name="Root Corp",
            type="Corporate",
            level=0,
            parent_id=None,
            is_active=True
        )
        db_session.add(corporate)
        db_session.commit()

        assert corporate.parent_id is None
        assert corporate.parent is None
        assert corporate.level == 0

    def test_inactive_children_filtering(self, db_session, sample_entities):
        """Test filtering active/inactive children"""
        plant_a = sample_entities["plant_a"]

        # Add inactive line
        inactive_line = Entity(
            name="Inactive Line",
            type="Line",
            level=2,
            parent_id=plant_a.id,
            is_active=False
        )
        db_session.add(inactive_line)
        db_session.commit()

        # Get active children only
        active_children = plant_a.get_all_children(active_only=True)
        all_children = plant_a.get_all_children(active_only=False)

        # Active should not include inactive line
        assert len(all_children) > len(active_children)
        assert inactive_line not in active_children
        assert inactive_line in all_children


class TestCircularReferencePrevention:
    """Test circular reference prevention"""

    def test_prevent_self_reference(self, db_session, sample_entities):
        """Test that entity cannot be its own parent"""
        plant_a = sample_entities["plant_a"]

        is_valid, error = validate_circular_reference(
            db_session,
            plant_a.id,
            plant_a.id
        )

        assert is_valid is False
        assert "cannot be its own parent" in error

    def test_prevent_child_as_parent(self, db_session, sample_entities):
        """Test that entity cannot have its child as parent"""
        plant_a = sample_entities["plant_a"]
        line_1 = sample_entities["line_1"]

        # Try to make Line 1 the parent of Plant A
        is_valid, error = validate_circular_reference(
            db_session,
            plant_a.id,
            line_1.id
        )

        assert is_valid is False
        assert "descendant" in error.lower()

    def test_prevent_grandchild_as_parent(self, db_session, sample_entities):
        """Test that entity cannot have its grandchild as parent"""
        plant_a = sample_entities["plant_a"]
        process_1 = sample_entities["process_1"]

        # Try to make Process 1 the parent of Plant A
        is_valid, error = validate_circular_reference(
            db_session,
            plant_a.id,
            process_1.id
        )

        assert is_valid is False
        assert "descendant" in error.lower()

    def test_is_descendant_of(self, db_session, sample_entities):
        """Test is_descendant_of method"""
        corporate = sample_entities["corporate"]
        plant_a = sample_entities["plant_a"]
        line_1 = sample_entities["line_1"]
        process_1 = sample_entities["process_1"]

        # Process 1 is descendant of all ancestors
        assert process_1.is_descendant_of(line_1) is True
        assert process_1.is_descendant_of(plant_a) is True
        assert process_1.is_descendant_of(corporate) is True

        # Line 1 is not descendant of Process 1
        assert line_1.is_descendant_of(process_1) is False

        # Siblings are not descendants of each other
        line_2 = sample_entities["line_2"]
        assert line_1.is_descendant_of(line_2) is False

    def test_valid_parent_change(self, db_session, sample_entities):
        """Test valid parent change is allowed"""
        line_2 = sample_entities["line_2"]
        plant_b = sample_entities["plant_b"]

        # Move Line 2 from Plant A to Plant B
        is_valid, error = validate_circular_reference(
            db_session,
            line_2.id,
            plant_b.id
        )

        assert is_valid is True
        assert error is None


class TestEntityValidation:
    """Test entity validation"""

    def test_level_validation(self, db_session):
        """Test level must be within valid range"""
        with pytest.raises(ValueError, match="Level must be between"):
            entity = Entity(
                name="Invalid Level",
                type="Corporate",
                level=10,  # Invalid level
                is_active=True
            )
            db_session.add(entity)
            db_session.flush()

    def test_type_validation(self, db_session):
        """Test type must be valid"""
        with pytest.raises(ValueError, match="Type must be one of"):
            entity = Entity(
                name="Invalid Type",
                type="InvalidType",
                level=0,
                is_active=True
            )
            db_session.add(entity)
            db_session.flush()

    def test_email_validation(self, db_session):
        """Test email validation"""
        with pytest.raises(ValueError, match="Invalid email format"):
            entity = Entity(
                name="Invalid Email",
                type="Corporate",
                level=0,
                email="not-an-email",  # Invalid email
                is_active=True
            )
            db_session.add(entity)
            db_session.flush()

    def test_valid_email(self, db_session):
        """Test valid email is accepted"""
        entity = Entity(
            name="Valid Email",
            type="Corporate",
            level=0,
            email="test@example.com",
            is_active=True
        )
        db_session.add(entity)
        db_session.commit()

        assert entity.email == "test@example.com"


class TestEntityHelpers:
    """Test utility helper functions"""

    def test_calculate_entity_level(self, db_session, sample_entities):
        """Test automatic level calculation from parent"""
        plant_a = sample_entities["plant_a"]

        calculated_level = calculate_entity_level(db_session, plant_a.id)

        assert calculated_level == 2  # Plant A is level 1, so child should be level 2

    def test_calculate_entity_level_root(self, db_session):
        """Test level calculation for root (no parent)"""
        calculated_level = calculate_entity_level(db_session, None)

        assert calculated_level == 0

    def test_build_entity_tree(self, db_session, sample_entities):
        """Test building hierarchical tree structure"""
        tree = build_entity_tree(db_session, parent_id=None, active_only=True)

        assert len(tree) == 1  # One root entity
        assert tree[0]['name'] == "Test Corp"
        assert len(tree[0]['children']) == 2  # Two plants

    def test_search_entities(self, db_session, sample_entities):
        """Test searching entities"""
        results = search_entities(db_session, "Plant", active_only=True)

        assert len(results) == 2
        assert all("Plant" in entity.name for entity in results)

    def test_search_entities_by_level(self, db_session, sample_entities):
        """Test searching entities by level"""
        results = search_entities(db_session, "", level=2, active_only=True)

        assert len(results) == 2  # Two lines at level 2
        assert all(entity.level == 2 for entity in results)


class TestEntityToDict:
    """Test entity serialization"""

    def test_to_dict(self, db_session, sample_entities):
        """Test converting entity to dictionary"""
        process_1 = sample_entities["process_1"]

        entity_dict = process_1.to_dict()

        assert entity_dict['id'] == process_1.id
        assert entity_dict['name'] == "Process 1"
        assert entity_dict['type'] == "Process"
        assert entity_dict['level'] == 3
        assert entity_dict['full_path'] == "Test Corp > Plant A > Line 1 > Process 1"
        assert 'created_at' in entity_dict
        assert 'can_have_children' in entity_dict
        assert 'expected_child_type' in entity_dict


class TestDatabaseConstraints:
    """Test database-level constraints"""

    def test_parent_deletion_restricted(self, db_session, sample_entities):
        """Test that parent cannot be deleted if it has children"""
        corporate = sample_entities["corporate"]

        # Try to delete corporate (has children)
        with pytest.raises(IntegrityError):
            db_session.delete(corporate)
            db_session.commit()

        db_session.rollback()

    def test_unique_not_enforced(self, db_session):
        """Test that names don't have to be unique (can have duplicate names)"""
        entity1 = Entity(
            name="Same Name",
            type="Corporate",
            level=0,
            is_active=True
        )
        entity2 = Entity(
            name="Same Name",
            type="Corporate",
            level=0,
            is_active=True
        )

        db_session.add_all([entity1, entity2])
        db_session.commit()

        # Should succeed - names are not unique
        assert entity1.id != entity2.id

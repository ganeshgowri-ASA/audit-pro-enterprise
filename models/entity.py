"""
Entity Model - Hierarchical Organization Structure

Supports 5 levels:
- Level 0: Corporate
- Level 1: Plant
- Level 2: Line
- Level 3: Process
- Level 4: Sub-Process
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, CheckConstraint, Index, Text
)
from sqlalchemy.orm import relationship, validates
from database.base import Base
from config.settings import ENTITY_TYPES, MAX_HIERARCHY_LEVEL


class Entity(Base):
    """
    Entity model representing hierarchical organizational structure.

    Attributes:
        id: Primary key
        name: Entity name
        type: Entity type (Corporate/Plant/Line/Process/Sub-Process)
        parent_id: Foreign key to parent entity
        level: Hierarchy level (0-4)
        location: Physical location
        address: Full address
        contact_person: Contact person name
        email: Contact email
        phone: Contact phone number
        is_active: Active status flag
        created_at: Creation timestamp
        updated_at: Last update timestamp
        description: Optional description
    """

    __tablename__ = "entities"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Basic information
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(50), nullable=False)

    # Hierarchy
    parent_id = Column(Integer, ForeignKey("entities.id", ondelete="RESTRICT"), nullable=True)
    level = Column(Integer, nullable=False, default=0)

    # Location details
    location = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)

    # Contact information
    contact_person = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

    # Status and metadata
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    parent = relationship("Entity", remote_side=[id], backref="children")

    # Constraints
    __table_args__ = (
        CheckConstraint(f"level >= 0 AND level <= {MAX_HIERARCHY_LEVEL}", name="check_level_range"),
        CheckConstraint("level = 0 AND parent_id IS NULL OR level > 0", name="check_root_no_parent"),
        Index("idx_entity_parent_level", "parent_id", "level"),
        Index("idx_entity_active", "is_active"),
    )

    @validates('level')
    def validate_level(self, key, value):
        """Validate level is within acceptable range"""
        if value < 0 or value > MAX_HIERARCHY_LEVEL:
            raise ValueError(f"Level must be between 0 and {MAX_HIERARCHY_LEVEL}")
        return value

    @validates('type')
    def validate_type(self, key, value):
        """Validate entity type matches the level"""
        valid_types = list(ENTITY_TYPES.values())
        if value not in valid_types:
            raise ValueError(f"Type must be one of: {', '.join(valid_types)}")
        return value

    @validates('email')
    def validate_email(self, key, value):
        """Basic email validation"""
        if value and '@' not in value:
            raise ValueError("Invalid email format")
        return value

    def get_full_path(self, separator: str = " > ") -> str:
        """
        Get full hierarchical path from root to this entity.

        Args:
            separator: String to separate entity names

        Returns:
            Full path string (e.g., "ABC Corp > Plant A > Line 1")
        """
        path = [self.name]
        current = self
        while current.parent:
            current = current.parent
            path.insert(0, current.name)
        return separator.join(path)

    def get_all_children(self, active_only: bool = True) -> List['Entity']:
        """
        Recursively get all children entities.

        Args:
            active_only: If True, return only active entities

        Returns:
            List of all descendant entities
        """
        all_children = []
        children = [c for c in self.children if not active_only or c.is_active]

        for child in children:
            all_children.append(child)
            all_children.extend(child.get_all_children(active_only))

        return all_children

    def get_ancestors(self) -> List['Entity']:
        """
        Get all ancestor entities from parent to root.

        Returns:
            List of ancestor entities
        """
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    def is_descendant_of(self, potential_ancestor: 'Entity') -> bool:
        """
        Check if this entity is a descendant of another entity.
        Used to prevent circular references.

        Args:
            potential_ancestor: Entity to check

        Returns:
            True if this entity is a descendant of potential_ancestor
        """
        current = self.parent
        while current:
            if current.id == potential_ancestor.id:
                return True
            current = current.parent
        return False

    def can_have_children(self) -> bool:
        """
        Check if entity can have children based on hierarchy level.

        Returns:
            True if entity can have children
        """
        return self.level < MAX_HIERARCHY_LEVEL

    def get_expected_child_type(self) -> Optional[str]:
        """
        Get the expected type for children of this entity.

        Returns:
            Expected child entity type or None if no children allowed
        """
        if not self.can_have_children():
            return None
        return ENTITY_TYPES.get(self.level + 1)

    def __repr__(self):
        return f"<Entity(id={self.id}, name='{self.name}', type='{self.type}', level={self.level})>"

    def to_dict(self):
        """Convert entity to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parent_id": self.parent_id,
            "level": self.level,
            "location": self.location,
            "address": self.address,
            "contact_person": self.contact_person,
            "email": self.email,
            "phone": self.phone,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "description": self.description,
            "full_path": self.get_full_path(),
            "can_have_children": self.can_have_children(),
            "expected_child_type": self.get_expected_child_type()
        }

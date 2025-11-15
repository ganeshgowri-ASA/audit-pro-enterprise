"""
Utility functions for Entity hierarchy management
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.entity import Entity
from config.settings import ENTITY_TYPES


def validate_circular_reference(
    session: Session,
    entity_id: Optional[int],
    parent_id: Optional[int]
) -> tuple[bool, Optional[str]]:
    """
    Validate that setting parent_id won't create a circular reference.

    Args:
        session: Database session
        entity_id: ID of the entity being updated (None for new entities)
        parent_id: Proposed parent ID

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not parent_id:
        return True, None

    if entity_id == parent_id:
        return False, "An entity cannot be its own parent"

    # For new entities, no circular reference possible
    if not entity_id:
        return True, None

    # Check if parent is a descendant of this entity
    entity = session.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        return False, "Entity not found"

    parent = session.query(Entity).filter(Entity.id == parent_id).first()
    if not parent:
        return False, "Parent entity not found"

    # Check if parent is a descendant
    if parent.is_descendant_of(entity):
        return False, f"Circular reference: {parent.name} is a descendant of {entity.name}"

    return True, None


def calculate_entity_level(session: Session, parent_id: Optional[int]) -> int:
    """
    Calculate entity level based on parent.

    Args:
        session: Database session
        parent_id: Parent entity ID

    Returns:
        Calculated level (0-4)
    """
    if not parent_id:
        return 0

    parent = session.query(Entity).filter(Entity.id == parent_id).first()
    if parent:
        return parent.level + 1
    return 0


def get_entity_type_for_level(level: int) -> str:
    """
    Get entity type name for a given level.

    Args:
        level: Hierarchy level (0-4)

    Returns:
        Entity type name
    """
    return ENTITY_TYPES.get(level, "Unknown")


def build_entity_tree(session: Session, parent_id: Optional[int] = None, active_only: bool = True) -> List[Dict[str, Any]]:
    """
    Build hierarchical tree structure of entities.

    Args:
        session: Database session
        parent_id: Parent entity ID (None for root entities)
        active_only: If True, include only active entities

    Returns:
        List of entity dictionaries with nested children
    """
    query = session.query(Entity).filter(Entity.parent_id == parent_id)

    if active_only:
        query = query.filter(Entity.is_active == True)

    entities = query.order_by(Entity.name).all()

    result = []
    for entity in entities:
        entity_dict = entity.to_dict()
        entity_dict['children'] = build_entity_tree(session, entity.id, active_only)
        result.append(entity_dict)

    return result


def get_entity_dropdown_options(
    session: Session,
    level: Optional[int] = None,
    active_only: bool = True,
    exclude_id: Optional[int] = None
) -> List[tuple[str, int]]:
    """
    Get entity options for dropdown selection.

    Args:
        session: Database session
        level: Filter by specific level (None for all levels)
        active_only: If True, include only active entities
        exclude_id: Exclude specific entity ID

    Returns:
        List of tuples (display_name, entity_id)
    """
    query = session.query(Entity)

    if level is not None:
        query = query.filter(Entity.level == level)

    if active_only:
        query = query.filter(Entity.is_active == True)

    if exclude_id:
        query = query.filter(Entity.id != exclude_id)

    entities = query.order_by(Entity.level, Entity.name).all()

    return [(f"{entity.get_full_path()} ({entity.type})", entity.id) for entity in entities]


def get_parent_candidates(
    session: Session,
    entity_id: Optional[int] = None,
    target_level: Optional[int] = None
) -> List[tuple[str, int]]:
    """
    Get valid parent candidates for an entity.

    Args:
        session: Database session
        entity_id: Current entity ID (None for new entities)
        target_level: Target level for the entity

    Returns:
        List of tuples (display_name, entity_id)
    """
    # Parent must be one level above
    if target_level is None or target_level == 0:
        return []

    parent_level = target_level - 1

    query = session.query(Entity).filter(
        Entity.level == parent_level,
        Entity.is_active == True
    )

    # Exclude entity itself and its descendants
    if entity_id:
        entity = session.query(Entity).filter(Entity.id == entity_id).first()
        if entity:
            descendant_ids = [e.id for e in entity.get_all_children(active_only=False)]
            descendant_ids.append(entity_id)
            query = query.filter(~Entity.id.in_(descendant_ids))

    entities = query.order_by(Entity.name).all()

    return [(f"{entity.get_full_path()} ({entity.type})", entity.id) for entity in entities]


def search_entities(
    session: Session,
    search_term: str,
    entity_type: Optional[str] = None,
    level: Optional[int] = None,
    active_only: bool = True
) -> List[Entity]:
    """
    Search entities by name, location, or contact person.

    Args:
        session: Database session
        search_term: Search term
        entity_type: Filter by entity type
        level: Filter by level
        active_only: If True, include only active entities

    Returns:
        List of matching entities
    """
    query = session.query(Entity)

    # Search in name, location, and contact_person
    search_filter = (
        Entity.name.ilike(f"%{search_term}%") |
        Entity.location.ilike(f"%{search_term}%") |
        Entity.contact_person.ilike(f"%{search_term}%")
    )
    query = query.filter(search_filter)

    if entity_type:
        query = query.filter(Entity.type == entity_type)

    if level is not None:
        query = query.filter(Entity.level == level)

    if active_only:
        query = query.filter(Entity.is_active == True)

    return query.order_by(Entity.level, Entity.name).all()


def export_entities_to_dict(session: Session, active_only: bool = True) -> List[Dict[str, Any]]:
    """
    Export all entities to list of dictionaries (for Excel export).

    Args:
        session: Database session
        active_only: If True, include only active entities

    Returns:
        List of entity dictionaries
    """
    query = session.query(Entity)

    if active_only:
        query = query.filter(Entity.is_active == True)

    entities = query.order_by(Entity.level, Entity.name).all()

    return [{
        "ID": e.id,
        "Name": e.name,
        "Type": e.type,
        "Level": e.level,
        "Full Path": e.get_full_path(),
        "Parent": e.parent.name if e.parent else "None",
        "Location": e.location or "",
        "Address": e.address or "",
        "Contact Person": e.contact_person or "",
        "Email": e.email or "",
        "Phone": e.phone or "",
        "Active": "Yes" if e.is_active else "No",
        "Created": e.created_at.strftime("%Y-%m-%d %H:%M:%S") if e.created_at else "",
        "Description": e.description or ""
    } for e in entities]


def get_entity_statistics(session: Session) -> Dict[str, Any]:
    """
    Get statistics about entities.

    Args:
        session: Database session

    Returns:
        Dictionary with statistics
    """
    total = session.query(Entity).count()
    active = session.query(Entity).filter(Entity.is_active == True).count()
    inactive = total - active

    by_level = {}
    for level, type_name in ENTITY_TYPES.items():
        count = session.query(Entity).filter(
            Entity.level == level,
            Entity.is_active == True
        ).count()
        by_level[type_name] = count

    return {
        "total": total,
        "active": active,
        "inactive": inactive,
        "by_type": by_level
    }

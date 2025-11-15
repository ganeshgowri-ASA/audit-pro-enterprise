"""
Entity Model
AuditPro Enterprise - Organizational hierarchy (Company -> Plant -> Department -> Process)
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Entity(BaseModel):
    """
    Entity model for organizational hierarchy
    Supports multi-level structure: Company -> Plant -> Department -> Process
    """
    __tablename__ = "entities"

    # Entity information
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    entity_type = Column(String(50), nullable=False)  # Company, Plant, Department, Process
    description = Column(Text)

    # Contact information
    manager_name = Column(String(100))
    manager_email = Column(String(100))
    location = Column(String(200))

    # Hierarchy
    parent_id = Column(Integer, ForeignKey("entities.id"), nullable=True)

    # Relationships
    parent = relationship("Entity", remote_side="Entity.id", backref="children")
    audits = relationship("Audit", back_populates="entity")

    def get_full_path(self):
        """
        Get full hierarchical path
        Example: "Company A / Plant B / Department C"
        """
        path = [self.name]
        current = self.parent
        while current:
            path.insert(0, current.name)
            current = current.parent
        return " / ".join(path)

    def get_hierarchy_level(self):
        """
        Get the level in hierarchy (0 = root)
        """
        level = 0
        current = self.parent
        while current:
            level += 1
            current = current.parent
        return level

    def __repr__(self):
        return f"<Entity(id={self.id}, code={self.code}, name={self.name}, type={self.entity_type})>"

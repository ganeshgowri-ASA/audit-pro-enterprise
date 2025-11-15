"""
NC/OFI Status Change History Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class NCOFIHistory(Base):
    __tablename__ = "nc_ofi_history"

    id = Column(Integer, primary_key=True, index=True)
    nc_ofi_id = Column(Integer, ForeignKey("nc_ofi.id"), nullable=False, index=True)
    changed_by_id = Column(Integer, ForeignKey("users.id"))
    old_status = Column(String(20))
    new_status = Column(String(20), nullable=False)
    comment = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    nc_ofi = relationship("NCOFI", backref="history")
    changed_by = relationship("User")

    def __repr__(self):
        return f"<NCOFIHistory: {self.old_status} -> {self.new_status}>"

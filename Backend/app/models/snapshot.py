from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)

    vm_id = Column(Integer, ForeignKey("virtual_machines.id"), nullable=False)

    snapshot_name = Column(String, nullable=False)

    description = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
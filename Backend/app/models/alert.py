from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    vm_id = Column(Integer, ForeignKey("virtual_machines.id"))

    title = Column(String, nullable=False)

    description = Column(String)

    severity = Column(String, nullable=False)

    status = Column(String, default="ACTIVE")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
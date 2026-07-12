from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    vm_id = Column(Integer, ForeignKey("virtual_machines.id"))

    event_type = Column(String, nullable=False)

    message = Column(String, nullable=False)

    severity = Column(String, default="INFO")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
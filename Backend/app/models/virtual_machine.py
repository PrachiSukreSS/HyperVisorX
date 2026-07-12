from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class VirtualMachine(Base):
    __tablename__ = "virtual_machines"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)
    uuid = Column(String, unique=True, nullable=False)

    os_type = Column(String, nullable=False)

    cpu = Column(Integer, nullable=False)

    memory = Column(Integer, nullable=False)

    disk_size = Column(Integer, nullable=False)

    status = Column(String, default="stopped")

    ip_address = Column(String)

    mac_address = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
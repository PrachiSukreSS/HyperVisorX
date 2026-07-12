"""
app/core/database.py
====================
SQLAlchemy engine, session factory, and declarative base.

WHY THIS EXISTS
---------------
Every module that needs DB access imports:
  - `get_db`    → FastAPI dependency that yields a request-scoped session
  - `Base`      → parent class for all ORM models
  - `engine`    → used by Alembic to run migrations

HOW IT FITS IN THE ARCHITECTURE
---------------------------------
  database.py  ←  imported by  →  models/ (Base)
                               →  services/ (get_db)
                               →  alembic/env.py (Base.metadata, engine)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# ------------------------------------------------------------------ #
# Engine                                                              #
# ------------------------------------------------------------------ #
# create_engine is a connection-pool factory; it does NOT open a
# connection immediately — it opens one lazily on the first query.
#
# pool_pre_ping=True: before handing a connection from the pool to a
# coroutine, SQLAlchemy sends a lightweight "SELECT 1" to verify the
# connection is still alive.  This prevents "connection already closed"
# errors after a PostgreSQL idle-timeout.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# ------------------------------------------------------------------ #
# Session factory                                                     #
# ------------------------------------------------------------------ #
# sessionmaker creates Session CLASSES (not instances).
# • autocommit=False → we control transactions explicitly
# • autoflush=False  → we flush manually (avoids accidental partial writes)
# • bind= was REMOVED in SQLAlchemy 2.0; pass engine to Session() or
#   use SessionLocal(bind=engine) at call site — handled below via get_db.
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,   # bind= is still valid for sessionmaker in SQLAlchemy 2.x;
                   # it was only removed from Session() direct instantiation.
)

# ------------------------------------------------------------------ #
# Declarative Base                                                    #
# ------------------------------------------------------------------ #
# SQLAlchemy 2.x canonical style: subclass DeclarativeBase.
# All ORM models inherit from Base — this registers them in
# Base.metadata so Alembic can detect them for autogenerate.
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every model file does::

        from app.core.database import Base

        class MyModel(Base):
            __tablename__ = "my_table"
            ...
    """
    pass


# ------------------------------------------------------------------ #
# FastAPI dependency                                                  #
# ------------------------------------------------------------------ #
from collections.abc import Generator
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a request-scoped database session.

    Usage in a router::

        from fastapi import Depends
        from app.core.database import get_db

        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...

    The `finally` block guarantees the session is closed (and the
    connection returned to the pool) even if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
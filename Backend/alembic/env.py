"""
alembic/env.py
==============
Alembic migration environment.

Key fixes applied:
  1. sys.path insert so `app.*` imports work when running `alembic` from Backend/
  2. settings.DATABASE_URL used DIRECTLY — never via config.set_main_option(),
     because ConfigParser treats `%` as a special interpolation character and
     chokes on percent-encoded URLs like vmadmin%40123.
  3. run_migrations_online uses create_engine(settings.DATABASE_URL) directly.
  4. All models imported before Base.metadata so Alembic detects them.
"""

import sys
import os
from logging.config import fileConfig
# pyrefly: ignore [missing-import]
from sqlalchemy import pool, create_engine
from alembic import context
from app.models.user import User      # noqa: F401
from app.models.virtual_machine import VirtualMachine   # noqa: F401
from app.models.snapshot import Snapshot    # noqa: F401
from app.models.event import Event   # noqa: F401
from app.models.alert import Alert      # noqa: F401
# ---------------------------------------------------
# ------------------------
# Ensure Backend/ is on sys.path so `app.*` imports resolve
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------------------------------------------------------
# Load application settings
# ---------------------------------------------------------------------------
from app.core.config import settings

# ---------------------------------------------------------------------------
# Alembic config object — access to values in alembic.ini
# ---------------------------------------------------------------------------
config = context.config

# NOTE: We intentionally do NOT call config.set_main_option("sqlalchemy.url", ...)
# here.  Python's ConfigParser (which backs Alembic config) treats `%` as a
# special interpolation character.  Percent-encoded URLs (e.g. %40 for @) will
# raise "invalid interpolation syntax".  Instead we pass the URL directly to
# create_engine() and context.configure() below.

# ---------------------------------------------------------------------------
# Python logging — reads from [loggers] section of alembic.ini
# ---------------------------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# Import ALL models so Alembic sees them in Base.metadata for autogenerate.
# Add new model imports here as you create them.
# ---------------------------------------------------------------------------
from app.core.database import Base
#from app.models.user import User  # noqa: F401

target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# Offline mode — generates SQL without a live DB connection
# ---------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """
    Run migrations without a live database connection.
    Useful for generating .sql scripts to review before applying.
    """
    context.configure(
        url=settings.DATABASE_URL,  # ← direct from settings, not config.get_main_option
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online mode — connects to DB and applies migrations
# ---------------------------------------------------------------------------
def run_migrations_online() -> None:
    """
    Run migrations with a live database connection.
    We create the engine directly from settings.DATABASE_URL.
    """
    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

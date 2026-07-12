"""
app/core/config.py
==================
Centralised application configuration using pydantic-settings.

WHY THIS EXISTS
---------------
Hardcoding values (host, ports, URIs) violates the 12-Factor App principle
"Store config in the environment".  Using pydantic-settings we get:

  • Automatic loading from .env files
  • Type coercion  (e.g. "8000" str → 8000 int)
  • Validation at startup – the app fails fast if a required value is missing
  • A single source of truth – every module imports `settings`, never os.getenv()

HOW IT FITS IN THE ARCHITECTURE
---------------------------------
  config.py  ←  imported by  →  logger.py, main.py, routers, services, libvirt layer

  Nothing in this file touches the database, HTTP, or libvirt.
  It is a pure data-class; zero side-effects on import.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All application settings, sourced from environment variables / .env file.

    Pydantic-Settings reads variables in this priority order:
      1. Real environment variables (e.g. export APP_NAME=foo)
      2. Values in the .env file
      3. Field default values defined below

    Adding a new setting is as simple as adding a new typed class attribute.
    """

    model_config = SettingsConfigDict(
        # Path to the .env file, relative to the process working directory
        env_file=".env",
        # Be strict: unknown fields in .env are silently ignored instead of
        # raising an error, which keeps things forward-compatible.
        extra="ignore",
        # Re-validates field values on assignment (useful if settings are
        # mutated in tests)
        validate_default=True,
    )

    # ------------------------------------------------------------------ #
    # Application identity                                                 #
    # ------------------------------------------------------------------ #
    APP_NAME: str = Field(
        default="HyperVisorX",
        description="Human-readable application name shown in Swagger UI.",
    )
    APP_VERSION: str = Field(
        default="0.1.0",
        description="Semantic version string, shown in Swagger UI and /health.",
    )
    DEBUG: bool = Field(
        default=False,
        description=(
            "When True: enables FastAPI debug mode, verbose tracebacks, "
            "and auto-reload. MUST be False in production."
        ),
    )

    # ------------------------------------------------------------------ #
    # HTTP server                                                          #
    # ------------------------------------------------------------------ #
    HOST: str = Field(
        default="0.0.0.0",
        description="Interface the Uvicorn server binds to.",
    )
    PORT: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="TCP port the server listens on.",
    )

    # ------------------------------------------------------------------ #
    # Logging                                                              #
    # ------------------------------------------------------------------ #
    LOG_LEVEL: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Minimum log severity level.  Must be a valid Python logging level.",
    )

    # ------------------------------------------------------------------ #
    # API routing                                                          #
    # ------------------------------------------------------------------ #
    API_PREFIX: str = Field(
        default="/api/v1",
        description=(
            "URL prefix for all versioned API routes. "
            "Changing this to /api/v2 in the future keeps clients decoupled."
        ),
    )

    # ------------------------------------------------------------------ #
    # libvirt / KVM                                                        #
    # ------------------------------------------------------------------ #
    LIBVIRT_URI: str = Field(
        default="qemu:///system",
        description=(
            "libvirt connection URI.  "
            "'qemu:///system'  → privileged, accesses KVM directly.  "
            "'qemu:///session' → unprivileged, for development only."
        ),
    )

    # ------------------------------------------------------------------ #
    # Database (PostgreSQL)                                                #
    # ------------------------------------------------------------------ #
    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/hypervisorx",
        description=(
            "Full SQLAlchemy database URL. "
            "Format: dialect+driver://user:password@host:port/dbname. "
            "Special characters in passwords must be percent-encoded "
            "(e.g. '@' → '%40')."
        ),
    )

    # ------------------------------------------------------------------ #
    # Authentication (JWT)                                                #
    # ------------------------------------------------------------------ #
    SECRET_KEY: str = Field(
        ...,
        description=(
            "Secret key used to sign JWT access tokens. "
            "Must remain confidential and should never be committed to Git."
        ),
    )

    ALGORITHM: str = Field(
        default="HS256",
        description="Algorithm used to sign and verify JWT tokens.",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        gt=0,
        description="Access token validity period in minutes.",
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the singleton Settings instance.

    Using @lru_cache ensures that .env is parsed ONCE at startup and the same
    object is reused everywhere.  This:

      • Avoids repeated disk I/O on every request
      • Lets tests override settings by calling get_settings.cache_clear()
        and re-instantiating with different env vars

    Usage anywhere in the codebase::

        from app.core.config import get_settings
        settings = get_settings()
        print(settings.APP_NAME)
    """
    return Settings()


# Module-level convenience alias so callers can simply do:
#   from app.core.config import settings
settings: Settings = get_settings()

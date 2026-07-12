"""
app/core/logger.py
==================
Centralised logging configuration for the entire application.

WHY THIS EXISTS
---------------
Python's logging module allows multiple "handlers" to receive the same log
record simultaneously.  Instead of calling `logging.basicConfig()` in every
module (which fights over the root logger configuration), we configure
everything once here and every other module just does:

    import logging
    logger = logging.getLogger(__name__)

This gives us:
  • Consistent format across the whole codebase
  • Log records sent to BOTH the console AND a rotating file simultaneously
  • Severity controlled by a single settings value (LOG_LEVEL)
  • Zero duplication

HOW IT FITS IN THE ARCHITECTURE
---------------------------------
  logger.py  ←  called once by  →  main.py (app startup)
               used by          →  every module via getLogger(__name__)

The logger is NOT a singleton object we pass around.  Python's logging system
is globally keyed by name, so `getLogger("app.api.health")` automatically
inherits the handlers set up here.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings

# ------------------------------------------------------------------ #
# Constants                                                           #
# ------------------------------------------------------------------ #

# A structured, human-readable format that works well in terminals and
# is also easy to parse with tools like grep or Loki.
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log files live in a `logs/` directory next to `backend/`.
# We resolve relative to this file's location so the path is always correct
# regardless of the process working directory.
_LOG_DIR = Path(__file__).resolve().parents[3] / "logs"
_LOG_FILE = _LOG_DIR / "app.log"

# Max size before the file is rotated, and how many backup files to keep.
_MAX_BYTES = 10 * 1024 * 1024   # 10 MB
_BACKUP_COUNT = 5                # keeps app.log, app.log.1 … app.log.5


def setup_logging() -> None:
    """
    Configure the root logger once at application startup.

    After this call every module can use::

        import logging
        logger = logging.getLogger(__name__)
        logger.info("Something happened")

    and the record will appear in both the terminal and in logs/app.log.

    Design decisions:
    -----------------
    - We configure the ROOT logger (``""``).  All child loggers (e.g.
      ``app.api.health``) inherit its level and handlers automatically.
    - ``propagate=True`` (the default) means child loggers send records up to
      the root, where our handlers pick them up.
    - ``RotatingFileHandler`` prevents the log file from growing unboundedly
      in production.
    - We silence overly-verbose third-party libraries (uvicorn access logs
      are useful but can be noisy at DEBUG level).
    """
    # Ensure the logs directory exists; create it if not.
    _LOG_DIR.mkdir(parents=True, exist_ok=True)

    numeric_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # --- Console handler ---------------------------------------------------
    # StreamHandler defaults to sys.stderr; we use sys.stdout so log lines
    # appear interleaved with normal print() output in order.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)

    # --- Rotating file handler ---------------------------------------------
    file_handler = RotatingFileHandler(
        filename=_LOG_FILE,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)

    # --- Root logger -------------------------------------------------------
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Avoid duplicate handlers if setup_logging() is called more than once
    # (can happen during testing or hot-reload).
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

    # --- Silence noisy third-party loggers ---------------------------------
    # uvicorn.access logs every HTTP request at INFO; our middleware will do
    # this instead so we avoid double-logging.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    # Pydantic's internal logger can be chatty in DEBUG mode.
    logging.getLogger("pydantic").setLevel(logging.WARNING)

    logging.getLogger(__name__).info(
        "Logging initialised | level=%s | file=%s",
        settings.LOG_LEVEL,
        _LOG_FILE,
    )

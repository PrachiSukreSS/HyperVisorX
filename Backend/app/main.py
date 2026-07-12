"""
app/main.py
===========
FastAPI application factory — the single entry point for the entire backend.

WHY THIS EXISTS
---------------
main.py is the composition root of the application.  Its only job is:

  1. Create the FastAPI app instance with metadata
  2. Register middleware (request logging, CORS, etc.)
  3. Register global exception handlers
  4. Mount all versioned routers
  5. Define startup / shutdown lifecycle hooks

It should contain NO business logic.  If you find yourself writing data
access or computation here, move it to a service.

HOW IT FITS IN THE ARCHITECTURE
---------------------------------
  Uvicorn  →  app (main.py)  →  Routers  →  Services  →  libvirt layer

  The app object created here is what Uvicorn receives as
  `uvicorn app.main:app`.  Every request flows through the middleware
  stack before reaching a router.
"""

import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import health as health_router
from app.core.config import settings
from app.core.logger import setup_logging
from app.routers.auth import router as auth_router
# ------------------------------------------------------------------ #
# Initialise logging FIRST, before anything else logs.               #
# ------------------------------------------------------------------ #
setup_logging()
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
# Lifespan — startup / shutdown events                               #
# ------------------------------------------------------------------ #

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application startup and shutdown using the modern lifespan API.

    FastAPI replaced the @app.on_event("startup") / @app.on_event("shutdown")
    decorators with the lifespan context manager (Python 3.10+).

    Everything BEFORE `yield` runs at startup.
    Everything AFTER  `yield` runs at shutdown.

    Future startup tasks (in order):
      - Validate libvirt connection
      - Initialise SQLAlchemy connection pool
      - Warm up Redis cache
      - Start background metric scrapers
    """
    # ---- Startup ---------------------------------------------------------
    logger.info("=" * 60)
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("Debug mode : %s", settings.DEBUG)
    logger.info("API prefix : %s", settings.API_PREFIX)
    logger.info("libvirt URI: %s", settings.LIBVIRT_URI)
    logger.info("=" * 60)

    yield  # ← Application is running and serving requests here

    # ---- Shutdown --------------------------------------------------------
    logger.info("Shutting down %s …", settings.APP_NAME)
    # Future: close libvirt connections, flush metrics, drain queues


# ------------------------------------------------------------------ #
# FastAPI application instance                                        #
# ------------------------------------------------------------------ #

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "**HyperVisorX** — Enterprise-grade KVM/libvirt Virtualization Management Platform.\n\n"
        "Manage Linux Virtual Machines, snapshots, storage, and networking "
        "from a single REST API.  Built on FastAPI, libvirt-python, and KVM.\n\n"
        "---\n"
        "**Architecture**: React → FastAPI → Services → libvirt → QEMU/KVM\n\n"
        "**Module 2**: Foundation — health check, configuration, logging.\n"
        "**Module 3**: VM lifecycle (create, start, stop, delete, restart …)\n"
    ),
    # Swagger UI lives at /docs; ReDoc lives at /redoc
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    # Semantic versioning — update when the contract changes
    contact={
        "name": "HyperVisorX",
        "url": "https://github.com/your-org/hypervisorx",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
    lifespan=lifespan,
)


# ------------------------------------------------------------------ #
# Middleware                                                          #
# ------------------------------------------------------------------ #

# CORS — allow the React frontend (different origin) to call the API.
# In production, replace ["*"] with the exact frontend URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Log every incoming HTTP request and its response.

    Assigns a unique X-Request-ID to each request so that log lines from
    the same request can be correlated across services (useful when we add
    a reverse proxy or distributed tracing later).

    Logs:
      → [method] [path] — on request arrival
      ← [status_code] in [duration]ms — on response

    Performance note: `await call_next(request)` is the actual handler.
    Code before it runs before the handler; code after runs after.
    """
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "→ %s %s | client=%s | request_id=%s",
        request.method,
        request.url.path,
        request.client.host if request.client else "unknown",
        request_id,
    )

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start_time) * 1000
    logger.info(
        "← %s %s | status=%d | duration=%.2fms | request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_id,
    )

    # Surface the request ID to clients so they can include it in bug reports.
    response.headers["X-Request-ID"] = request_id
    return response


# ------------------------------------------------------------------ #
# Global exception handlers                                          #
# ------------------------------------------------------------------ #

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for any unhandled exception that escapes a route.

    Without this, FastAPI returns a generic 500 with an HTML body.
    This ensures ALL error responses are JSON, consistent with the
    rest of the API — critical for client-side parsing.

    In DEBUG mode we include the exception message; in production we hide
    it to avoid leaking internal details.
    """
    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.url.path,
    )

    detail = str(exc) if settings.DEBUG else "An internal server error occurred."

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "detail": detail,
            "path": str(request.url.path),
        },
    )


# ------------------------------------------------------------------ #
# Router registration                                                 #
# ------------------------------------------------------------------ #
# Every router is mounted under the versioned API prefix.
# Adding v2 routes in the future means a new prefix — zero migration work.

app.include_router(
    health_router.router,
    prefix=settings.API_PREFIX,   # → /api/v1/health
)
app.include_router(
    auth_router,
    prefix=settings.API_PREFIX,
)
# Future routers (will be added in coming modules):
# app.include_router(vms_router.router,      prefix=settings.API_PREFIX)
# app.include_router(hosts_router.router,    prefix=settings.API_PREFIX)
# app.include_router(storage_router.router,  prefix=settings.API_PREFIX)
# app.include_router(network_router.router,  prefix=settings.API_PREFIX)
# app.include_router(snapshots_router.router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {
        "application": "HyperVisorX",
        "version": "0.1.0",
        "status": "Running"
    }
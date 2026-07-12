"""
app/api/v1/health.py
=====================
Health-check router — the first and simplest API endpoint.

WHY THIS EXISTS
---------------
A health-check endpoint is a fundamental requirement for any production
service.  It is used by:
  • Load balancers  (AWS ALB, GCP LB, nginx) to decide whether to route
    traffic to this instance
  • Container orchestrators (Kubernetes liveness/readiness probes)
  • Monitoring systems (Prometheus blackbox exporter, uptime monitors)
  • Developers  — the first thing you curl after deployment

HOW IT FITS IN THE ARCHITECTURE
---------------------------------
Router  →  (no service layer needed here, logic is trivial)  →  Returns schema

In future modules, the health router will call a HealthService that pings
the database and the libvirt daemon so the response can say:
  {
    "status": "healthy",
    "database": "connected",
    "libvirt": "connected"
  }
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.health import HealthResponse

# Every module gets its own named logger.
# The name "app.api.v1.health" appears in log lines so we know exactly
# which module generated the log record.
logger = logging.getLogger(__name__)

# APIRouter is FastAPI's way of grouping related endpoints.
# The `tags` argument groups these routes in Swagger UI.
router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Application health check",
    description=(
        "Returns the current operational status of the HyperVisorX API. "
        "A 200 response with status='healthy' means the server is running and "
        "able to handle requests.  Future versions will include database and "
        "libvirt connectivity checks."
    ),
    # HTTP 200 is the only expected success code for a health check.
    status_code=200,
)
async def get_health() -> HealthResponse:
    """
    Perform an application-level health check.

    This is intentionally lightweight — it must respond quickly even when
    the system is under load.  Database and external service checks will be
    added as separate endpoints (e.g. /health/ready) in Module 3.

    Returns
    -------
    HealthResponse
        A JSON object with the service status, version, and current UTC time.
    """
    logger.debug("Health check requested")

    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        # timezone.utc ensures the timestamp is always UTC, never wall-clock
        # local time — critical for distributed systems.
        timestamp=datetime.now(tz=timezone.utc),
    )

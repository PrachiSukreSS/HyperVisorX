"""
app/schemas/health.py
=====================
Pydantic response schema for the health-check endpoint.

WHY THIS EXISTS
---------------
Schemas define the contract between the API and its clients.
Separating schemas from routes keeps routers thin and makes the
contract independently testable and reusable.

Even a simple status field lives in a schema so that we can:
  • Auto-generate accurate OpenAPI documentation
  • Add fields (latency, db status, libvirt status) later without
    touching the router
"""

from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Response body returned by GET /api/v1/health.

    Fields are intentionally minimal for Module 2; they will be expanded
    in future modules to include:
      - database connectivity status
      - libvirt daemon reachability
      - individual component latencies
    """

    status: str = Field(
        description="Overall service status.  'healthy' means the API is up.",
        examples=["healthy"],
    )
    app_name: str = Field(
        description="Human-readable application name, sourced from settings.",
        examples=["HyperVisorX"],
    )
    version: str = Field(
        description="Running application version (semantic version string).",
        examples=["0.1.0"],
    )
    timestamp: datetime = Field(
        description="UTC timestamp at the moment the health check was evaluated.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "app_name": "HyperVisorX",
                    "version": "0.1.0",
                    "timestamp": "2026-07-11T12:00:00Z",
                }
            ]
        }
    }

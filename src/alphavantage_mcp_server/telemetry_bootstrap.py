"""
Telemetry Bootstrap Module

This module initializes Prometheus metrics for the AlphaVantage MCP server.
It provides centralized configuration and setup for telemetry components.
"""

import os
import logging
import threading
from typing import Optional
from prometheus_client import Counter, Histogram, Gauge, start_http_server

logger = logging.getLogger(__name__)

# Environment variable configuration
MCP_TELEMETRY_ENABLED = os.getenv("MCP_TELEMETRY_ENABLED", "true").lower() == "true"
MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME", "alphavantage")
MCP_SERVER_VERSION = os.getenv("MCP_SERVER_VERSION", "dev")
MCP_METRICS_PORT = int(os.getenv("MCP_METRICS_PORT", "9464"))

# Global telemetry state
_telemetry_initialized = False
_metrics_server_started = False
_metrics_server_thread: Optional[threading.Thread] = None

# Prometheus metrics - these will be initialized in init_telemetry()
MCP_CALLS: Optional[Counter] = None
MCP_ERRS: Optional[Counter] = None
MCP_LAT: Optional[Histogram] = None
MCP_REQ_B: Optional[Histogram] = None
MCP_RES_B: Optional[Histogram] = None
MCP_CONC: Optional[Gauge] = None


def _create_prometheus_metrics():
    """Create and return Prometheus metrics objects."""
    global MCP_CALLS, MCP_ERRS, MCP_LAT, MCP_REQ_B, MCP_RES_B, MCP_CONC

    MCP_CALLS = Counter(
        "mcp_tool_calls_total",
        "Total number of MCP tool calls",
        ["tool", "server", "version", "outcome"],
    )

    MCP_ERRS = Counter(
        "mcp_tool_errors_total",
        "Total number of MCP tool errors",
        ["tool", "error_kind"],
    )

    MCP_LAT = Histogram(
        "mcp_tool_latency_seconds",
        "MCP tool call latency in seconds",
        ["tool", "server", "version"],
        buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    )

    MCP_REQ_B = Histogram(
        "mcp_tool_request_bytes",
        "MCP tool request size in bytes",
        ["tool"],
        buckets=[64, 256, 1024, 4096, 16384, 65536, 262144, 1048576],
    )

    MCP_RES_B = Histogram(
        "mcp_tool_response_bytes",
        "MCP tool response size in bytes",
        ["tool"],
        buckets=[64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304],
    )

    MCP_CONC = Gauge(
        "mcp_tool_active_concurrency",
        "Number of currently active MCP tool calls",
        ["tool"],
    )


def _start_metrics_server():
    """Start the Prometheus metrics HTTP server."""
    global _metrics_server_started, _metrics_server_thread

    if _metrics_server_started:
        return

    try:

        def run_server():
            try:
                start_http_server(MCP_METRICS_PORT, addr="127.0.0.1")
                logger.info(
                    f"Prometheus metrics server started on 127.0.0.1:{MCP_METRICS_PORT}"
                )
            except Exception as e:
                logger.error(f"Failed to start metrics server: {e}")

        _metrics_server_thread = threading.Thread(target=run_server, daemon=True)
        _metrics_server_thread.start()
        _metrics_server_started = True

    except Exception as e:
        logger.error(f"Failed to start metrics server thread: {e}")


def init_telemetry(start_metrics: bool = True) -> None:
    """
    Initialize telemetry system.

    Args:
        start_metrics: Whether to start the Prometheus metrics HTTP server.
                      Set to False for Lambda environments.
    """
    global _telemetry_initialized

    if _telemetry_initialized:
        logger.debug("Telemetry already initialized")
        return

    if not MCP_TELEMETRY_ENABLED:
        logger.info("Telemetry disabled via MCP_TELEMETRY_ENABLED")
        return

    try:
        logger.info(
            f"Initializing telemetry for {MCP_SERVER_NAME} v{MCP_SERVER_VERSION}"
        )

        # Initialize Prometheus metrics
        _create_prometheus_metrics()
        logger.debug("Prometheus metrics created")

        # Start metrics server if requested
        if start_metrics:
            _start_metrics_server()

        _telemetry_initialized = True
        logger.info("Telemetry initialization complete")

    except Exception as e:
        logger.error(f"Failed to initialize telemetry: {e}")
        raise


def is_telemetry_enabled() -> bool:
    """Check if telemetry is enabled and initialized."""
    return MCP_TELEMETRY_ENABLED and _telemetry_initialized


# Export the metric objects for use by other modules
__all__ = [
    "init_telemetry",
    "is_telemetry_enabled",
    "MCP_CALLS",
    "MCP_ERRS",
    "MCP_LAT",
    "MCP_REQ_B",
    "MCP_RES_B",
    "MCP_CONC",
    "MCP_SERVER_NAME",
    "MCP_SERVER_VERSION",
]

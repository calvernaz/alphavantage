"""
Telemetry Instrumentation Module

This module provides the @instrument_tool decorator for wrapping MCP tool functions
with telemetry collection using Prometheus metrics.
"""

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Optional

from .telemetry_bootstrap import (
    MCP_CALLS,
    MCP_ERRS,
    MCP_LAT,
    MCP_REQ_B,
    MCP_RES_B,
    MCP_CONC,
    is_telemetry_enabled,
)

logger = logging.getLogger(__name__)


def _classify_error(error: Exception) -> str:
    """
    Classify an error into a category for metrics labeling.

    Args:
        error: The exception to classify

    Returns:
        Error category string: "timeout", "bad_input", "connection", or "unknown"
    """
    if isinstance(error, (TimeoutError, asyncio.TimeoutError)):
        return "timeout"
    elif isinstance(error, (ValueError, TypeError, KeyError, AttributeError)):
        return "bad_input"
    elif isinstance(error, (ConnectionError, OSError)):
        return "connection"
    else:
        return "unknown"


def _get_size_bytes(obj: Any) -> int:
    """
    Calculate the approximate size of an object in bytes.

    Args:
        obj: Object to measure

    Returns:
        Size in bytes (0 if measurement fails)
    """
    try:
        if obj is None:
            return 0
        elif isinstance(obj, (str, bytes)):
            return len(obj)
        else:
            # For other objects, convert to string and measure
            return len(str(obj))
    except Exception:
        return 0


def instrument_tool(tool_name: str, transport: Optional[str] = None) -> Callable:
    """
    Decorator to instrument MCP tool functions with telemetry collection.

    This decorator:
    - Increments/decrements active concurrency gauge
    - Measures execution duration
    - Classifies and counts errors
    - Emits calls_total metric with outcome
    - Measures request and response payload sizes

    Args:
        tool_name: Name of the tool for metrics labeling
        transport: Transport type ("stdio", "http", etc.) for metrics labeling

    Returns:
        Decorated function with telemetry instrumentation
    """

    def decorator(func: Callable) -> Callable:
        if not is_telemetry_enabled():
            # If telemetry is disabled, return the original function unchanged
            return func

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            """Async wrapper for instrumented functions."""
            start_time = time.time()
            outcome = "error"
            error_kind = None

            # Increment active concurrency
            if MCP_CONC:
                MCP_CONC.labels(tool=tool_name).inc()

            try:
                # Measure request size (approximate)
                request_data = {"args": args, "kwargs": kwargs}
                request_size = _get_size_bytes(request_data)
                if MCP_REQ_B:
                    MCP_REQ_B.labels(tool=tool_name).observe(request_size)

                # Execute the actual function
                result = await func(*args, **kwargs)

                # Measure response size
                response_size = _get_size_bytes(result)
                if MCP_RES_B:
                    MCP_RES_B.labels(tool=tool_name).observe(response_size)

                outcome = "ok"
                return result

            except Exception as e:
                error_kind = _classify_error(e)

                # Increment error counter
                if MCP_ERRS:
                    MCP_ERRS.labels(tool=tool_name, error_kind=error_kind).inc()

                logger.warning(f"Tool {tool_name} failed with {error_kind} error: {e}")
                raise

            finally:
                # Record execution time
                duration = time.time() - start_time
                if MCP_LAT:
                    MCP_LAT.labels(tool=tool_name).observe(duration)

                # Increment total calls counter
                if MCP_CALLS:
                    MCP_CALLS.labels(tool=tool_name, outcome=outcome).inc()

                # Decrement active concurrency
                if MCP_CONC:
                    MCP_CONC.labels(tool=tool_name).dec()

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            """Sync wrapper for instrumented functions."""
            start_time = time.time()
            outcome = "error"
            error_kind = None

            # Increment active concurrency
            if MCP_CONC:
                MCP_CONC.labels(tool=tool_name).inc()

            try:
                # Measure request size (approximate)
                request_data = {"args": args, "kwargs": kwargs}
                request_size = _get_size_bytes(request_data)
                if MCP_REQ_B:
                    MCP_REQ_B.labels(tool=tool_name).observe(request_size)

                # Execute the actual function
                result = func(*args, **kwargs)

                # Measure response size
                response_size = _get_size_bytes(result)
                if MCP_RES_B:
                    MCP_RES_B.labels(tool=tool_name).observe(response_size)

                outcome = "ok"
                return result

            except Exception as e:
                error_kind = _classify_error(e)

                # Increment error counter
                if MCP_ERRS:
                    MCP_ERRS.labels(tool=tool_name, error_kind=error_kind).inc()

                logger.warning(f"Tool {tool_name} failed with {error_kind} error: {e}")
                raise

            finally:
                # Record execution time
                duration = time.time() - start_time
                if MCP_LAT:
                    MCP_LAT.labels(tool=tool_name).observe(duration)

                # Increment total calls counter
                if MCP_CALLS:
                    MCP_CALLS.labels(tool=tool_name, outcome=outcome).inc()

                # Decrement active concurrency
                if MCP_CONC:
                    MCP_CONC.labels(tool=tool_name).dec()

        # Return appropriate wrapper based on whether function is async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Export the decorator
__all__ = ["instrument_tool"]

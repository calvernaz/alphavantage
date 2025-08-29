"""
Unit tests for telemetry modules.
"""

import sys
from unittest.mock import patch, MagicMock

import pytest

# Mock the external dependencies
sys.modules["prometheus_client"] = MagicMock()


class TestTelemetryInstrumentation:
    """Test telemetry instrumentation functionality."""

    def test_instrument_tool_decorator_disabled(self):
        """Test that decorator does nothing when telemetry is disabled."""
        with patch(
            "src.alphavantage_mcp_server.telemetry_instrument.is_telemetry_enabled",
            return_value=False,
        ):
            from src.alphavantage_mcp_server.telemetry_instrument import instrument_tool

            @instrument_tool("test_tool")
            def test_function(x, y):
                return x + y

            result = test_function(2, 3)
            assert result == 5

    def test_error_classification(self):
        """Test error classification logic."""
        from src.alphavantage_mcp_server.telemetry_instrument import _classify_error

        assert _classify_error(TimeoutError()) == "timeout"
        assert _classify_error(ValueError()) == "bad_input"
        assert _classify_error(TypeError()) == "bad_input"
        assert _classify_error(KeyError()) == "bad_input"
        assert _classify_error(ConnectionError()) == "connection"
        assert _classify_error(RuntimeError()) == "unknown"

    def test_size_calculation(self):
        """Test size calculation function."""
        from src.alphavantage_mcp_server.telemetry_instrument import _get_size_bytes

        assert _get_size_bytes("hello") == 5
        assert _get_size_bytes(b"hello") == 5
        assert _get_size_bytes(None) == 0
        assert _get_size_bytes(123) > 0


if __name__ == "__main__":
    pytest.main([__file__])

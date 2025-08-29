import asyncio
import json
import subprocess
import sys

import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


@pytest.mark.asyncio
async def test_http_transport_with_mcp_client():
    """Test HTTP transport using proper MCP streamable HTTP client"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8087",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        base_url = "http://localhost:8087/"

        client = streamablehttp_client(base_url + "mcp")

        async with client as streams:
            # Extract streams from the context
            if len(streams) == 3:
                read_stream, write_stream, session_manager = streams
            else:
                read_stream, write_stream = streams

            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the session
                init_result = await session.initialize()
                assert init_result is not None
                assert init_result.serverInfo.name == "alphavantage"

                # List available tools
                response = await session.list_tools()
                tools = response.tools
                tool_names = [tool.name for tool in tools]

                # Verify essential tools are present
                assert "stock_quote" in tool_names
                assert len(tools) > 0

                # Test calling the stock_quote tool
                result = await session.call_tool("stock_quote", {"symbol": "AAPL"})

                # Verify we got a result
                assert result is not None
                assert hasattr(result, "content")
                assert len(result.content) > 0

                # Parse the JSON result
                content_text = result.content[0].text
                stock_data = json.loads(content_text)

                assert "Global Quote" in stock_data or "Error Message" in stock_data
                assert stock_data["Global Quote"]["01. symbol"] == "AAPL"

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()


@pytest.mark.asyncio
async def test_http_transport_tool_listing():
    """Test HTTP transport tool listing functionality"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8088",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        base_url = "http://localhost:8088/"

        client = streamablehttp_client(base_url + "mcp")

        async with client as streams:
            if len(streams) == 3:
                read_stream, write_stream, session_manager = streams
            else:
                read_stream, write_stream = streams

            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                response = await session.list_tools()
                tools = response.tools

                # Verify we have tools
                assert len(tools) > 0

                # Verify essential tools are present
                tool_names = [tool.name for tool in tools]
                expected_tools = ["stock_quote", "time_series_daily"]

                for expected_tool in expected_tools:
                    assert expected_tool in tool_names, (
                        f"{expected_tool} not found in tools"
                    )

                # Verify each tool has required attributes
                for tool in tools:
                    assert hasattr(tool, "name")
                    assert hasattr(tool, "description")
                    assert hasattr(tool, "inputSchema")
                    assert tool.name is not None
                    assert tool.description is not None
                    assert tool.inputSchema is not None

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()


@pytest.mark.asyncio
async def test_http_transport_tool_call():
    """Test HTTP transport tool calling functionality"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8089",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        base_url = "http://localhost:8089/"

        client = streamablehttp_client(base_url + "mcp")

        async with client as streams:
            if len(streams) == 3:
                read_stream, write_stream, session_manager = streams
            else:
                read_stream, write_stream = streams

            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the session
                await session.initialize()

                # Call the stock_quote tool
                stock_result = await session.call_tool(
                    "stock_quote", {"symbol": "MSFT"}
                )

                # Verify we got a result
                assert stock_result is not None
                assert hasattr(stock_result, "content")
                assert len(stock_result.content) > 0

                # Parse and validate the result
                stock_content = stock_result.content[0].text
                stock_data = json.loads(stock_content)
                assert "Global Quote" in stock_data
                assert stock_data["Global Quote"]["01. symbol"] == "MSFT"

                # Call time_series_daily tool
                time_series_result = await session.call_tool(
                    "time_series_daily", {"symbol": "IBM", "outputsize": "compact"}
                )

                # Verify we got a result
                assert time_series_result is not None
                assert hasattr(time_series_result, "content")
                assert len(time_series_result.content) > 0

                # Parse and validate the result
                ts_content = time_series_result.content[0].text
                ts_data = json.loads(ts_content)
                assert "Time Series (Daily)" in ts_data
                assert "Meta Data" in ts_data
                assert ts_data["Meta Data"]["2. Symbol"] == "IBM"

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

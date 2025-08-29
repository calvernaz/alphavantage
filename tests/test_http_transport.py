import asyncio
import json
import subprocess
import sys

import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


@pytest.mark.asyncio
async def test_http_stock_quote():
    """Test streamable-http transport with stock_quote tool"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8091",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        base_url = "http://localhost:8091/"

        # Connect to the server using streamable-http client
        client = streamablehttp_client(base_url + "mcp")

        async with client as streams:
            # Handle different return formats from the client
            if len(streams) == 3:
                read_stream, write_stream, session_manager = streams
            else:
                read_stream, write_stream = streams

            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the session
                await session.initialize()

                # List available tools
                response = await session.list_tools()
                tools = response.tools
                tool_names = [tool.name for tool in tools]

                # Verify stock_quote tool is available
                assert "stock_quote" in tool_names, (
                    f"stock_quote not found in tools: {tool_names}"
                )

                # Test calling the stock_quote tool
                result = await session.call_tool("stock_quote", {"symbol": "AAPL"})

                # Verify we got a result
                assert result is not None
                assert hasattr(result, "content")
                assert len(result.content) > 0

                # Parse the JSON result to verify it contains stock data
                content_text = result.content[0].text
                stock_data = json.loads(content_text)

                # Verify the response contains expected stock quote fields
                assert "Global Quote" in stock_data or "Error Message" in stock_data

                if "Global Quote" in stock_data:
                    global_quote = stock_data["Global Quote"]
                    assert "01. symbol" in global_quote
                    assert "05. price" in global_quote
                    assert global_quote["01. symbol"] == "AAPL"

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()


@pytest.mark.asyncio
async def test_http_tool_list():
    """Test that streamable-http transport can list all available tools"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8092",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        base_url = "http://localhost:8092/"

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
async def test_http_multiple_calls():
    """Test making multiple tool calls over streamable-http transport"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8093",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        base_url = "http://localhost:8093/"

        client = streamablehttp_client(base_url + "mcp")

        async with client as streams:
            if len(streams) == 3:
                read_stream, write_stream, session_manager = streams
            else:
                read_stream, write_stream = streams

            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # Make multiple calls to test session persistence
                symbols = ["AAPL", "GOOGL", "MSFT"]
                results = []

                for symbol in symbols:
                    result = await session.call_tool("stock_quote", {"symbol": symbol})
                    assert result is not None
                    assert hasattr(result, "content")
                    assert len(result.content) > 0

                    content_text = result.content[0].text
                    stock_data = json.loads(content_text)
                    results.append(stock_data)

                # Verify we got results for all symbols
                assert len(results) == len(symbols)

                # Verify each result contains stock data or error message
                for i, result in enumerate(results):
                    assert "Global Quote" in result or "Error Message" in result, (
                        f"Invalid result for {symbols[i]}"
                    )

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()


@pytest.mark.asyncio
async def test_http_server_info():
    """Test retrieving server information over streamable-http transport"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8094",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        base_url = "http://localhost:8094/"

        client = streamablehttp_client(base_url + "mcp")

        async with client as streams:
            if len(streams) == 3:
                read_stream, write_stream, session_manager = streams
            else:
                read_stream, write_stream = streams

            async with ClientSession(read_stream, write_stream) as session:
                # Initialize and get server info
                init_result = await session.initialize()

                # Verify server info is present
                assert hasattr(init_result, "serverInfo")
                assert init_result.serverInfo.name == "alphavantage"
                assert init_result.serverInfo.version is not None

                # Verify protocol version
                assert init_result.protocolVersion is not None

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

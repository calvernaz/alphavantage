import asyncio
import json
import subprocess
import sys

import httpx
import pytest
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


@pytest.mark.asyncio
async def test_stdio_basic_connection():
    """Test basic stdio connection and tool listing"""

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "stdio",
        ],
    )

    client = stdio_client(server_params)
    async with client as (read_stream, write_stream):
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


@pytest.mark.asyncio
async def test_http_basic_connection():
    """Test basic HTTP connection using direct HTTP requests"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8084",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        # Test basic HTTP endpoint
        async with httpx.AsyncClient() as client:
            # Test initialization request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"},
                },
            }

            response = await client.post(
                "http://localhost:8084/mcp",
                json=init_request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "MCP-Protocol-Version": "2025-06-18",
                },
                timeout=10.0,
            )

            assert response.status_code == 200

            json_data = response.json()
            assert json_data is not None
            assert "result" in json_data
            assert json_data["result"]["serverInfo"]["name"] == "alphavantage"

            # Send initialized notification (required after initialize)
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
            }

            await client.post(
                "http://localhost:8084/mcp",
                json=initialized_notification,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "MCP-Protocol-Version": "2025-06-18",
                },
                timeout=10.0,
            )

            # Test tools/list request
            # https://modelcontextprotocol.io/specification/2025-06-18/server/tools#listing-tools
            tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

            response = await client.post(
                "http://localhost:8084/mcp",
                json=tools_request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "MCP-Protocol-Version": "2025-06-18",
                },
                timeout=10.0,
            )

            assert response.status_code == 200

            json_data = response.json()
            assert json_data is not None
            assert "result" in json_data
            assert "tools" in json_data["result"]

            tools = json_data["result"]["tools"]
            tool_names = [tool["name"] for tool in tools]
            assert "stock_quote" in tool_names
            assert len(tools) > 0

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()


@pytest.mark.asyncio
async def test_stdio_stock_quote_call():
    """Test calling STOCK_QUOTE tool via stdio"""

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "stdio",
        ],
    )

    client = stdio_client(server_params)
    async with client as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize
            await session.initialize()

            # Call stock_quote tool
            result = await session.call_tool("stock_quote", {"symbol": "AAPL"})

            # Verify we got a result
            assert result is not None
            assert hasattr(result, "content")
            assert len(result.content) > 0

            # Parse the JSON result
            content_text = result.content[0].text
            stock_data = json.loads(content_text)

            # Should contain either valid data or error message
            assert "Global Quote" in stock_data or "Error Message" in stock_data


@pytest.mark.asyncio
async def test_http_stock_quote_call():
    """Test calling STOCK_QUOTE tool via HTTP"""

    # Start the HTTP server
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "http",
            "--port",
            "8085",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give server time to start
        await asyncio.sleep(4)

        async with httpx.AsyncClient() as client:
            # Initialize first
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"},
                },
            }

            await client.post(
                "http://localhost:8085/mcp",
                json=init_request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
                timeout=10.0,
            )

            # Send initialized notification
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
            }

            await client.post(
                "http://localhost:8085/mcp",
                json=initialized_notification,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
                timeout=10.0,
            )

            # Call stock_quote tool
            tool_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "stock_quote", "arguments": {"symbol": "AAPL"}},
            }

            response = await client.post(
                "http://localhost:8085/mcp",
                json=tool_request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
                timeout=30.0,
            )

            assert response.status_code == 200

            # Parse SSE response for tool call
            json_data = response.json()
            assert json_data is not None
            assert "result" in json_data
            assert "content" in json_data["result"]

            content = json_data["result"]["content"]
            assert len(content) > 0

            # Parse the JSON result
            content_text = content[0]["text"]
            stock_data = json.loads(content_text)

            # Should contain either valid data or error message
            assert "Global Quote" in stock_data or "Error Message" in stock_data

    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

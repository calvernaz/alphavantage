import json
import sys

import pytest
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


@pytest.mark.asyncio
async def test_stdio_stock_quote():
    """Test stdio transport with stock_quote tool"""

    # Start the MCP server as a subprocess
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-c",
            "import sys; sys.path.insert(0, 'src'); from alphavantage_mcp_server import main; main()",
            "--server",
            "stdio",
        ],
    )

    # Connect to the server using stdio client
    client = stdio_client(server_params)
    async with client as (read_stream, write_stream):
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

            # Find the stock_quote tool
            next(tool for tool in tools if tool.name == "stock_quote")

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


@pytest.mark.asyncio
async def test_stdio_tool_list():
    """Test that stdio transport can list all available tools"""

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

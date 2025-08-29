import os
import sys
import json
import asyncio
from typing import Optional, Literal
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client

from openai import OpenAI

BASE_URL = "http://localhost:8080/"


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    async def connect_to_server(
        self, server_protocol: Literal["sse", "streamable-http"]
    ):
        """Connect to an MCP server"""
        if server_protocol == "sse":
            client = sse_client(BASE_URL + "sse")
            rs, ws = await self.exit_stack.enter_async_context(client)
        elif server_protocol == "streamable-http":
            client = streamablehttp_client(BASE_URL + "mcp")
            rs, ws, _ = await self.exit_stack.enter_async_context(client)
        else:
            raise Exception("Unknown transport protocol")
        self.session = await self.exit_stack.enter_async_context(ClientSession(rs, ws))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools_definitions
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using LLM and available tools"""
        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()
        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in response.tools
        ]

        # Initial LLM API call
        response = self.client.chat.completions.create(
            model=self.client.models.list().data[0].id,
            messages=messages,
            tools=available_tools,
            tool_choice="auto",
        )

        # Process response and handle tool calls
        final_text = []

        content = response.choices[0].message.content
        final_text.append(content)

        if response.choices[0].message.tool_calls:
            for tc in response.choices[0].message.tool_calls:
                f = tc.function
                tool_name = f.name
                tool_args = f.arguments

                # Execute tool call
                result = await self.session.call_tool(tool_name, json.loads(tool_args))
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # Continue conversation with tool results
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": result.content})

            # Get next response from LLM
            response = self.client.chat.completions.create(
                model=self.client.models.list().data[0].id,
                messages=messages,
            )

            final_text.append(response.choices[0].message.content)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                raise e
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def start():
    if len(sys.argv) == 2 and sys.argv[1] in ("sse", "streamable-http"):
        client = MCPClient()
        try:
            await client.connect_to_server(sys.argv[1])
            await client.chat_loop()
        finally:
            await client.cleanup()
    else:
        raise Exception("Usage: uv run client sse|streamable-http")


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()

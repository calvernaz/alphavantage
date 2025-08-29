"""
AWS Lambda function for stateless AlphaVantage MCP Server.
Based on aws-samples/sample-serverless-mcp-servers/stateless-mcp-on-lambda-python pattern.
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict

# Add the source directory to Python path for imports
sys.path.insert(0, "/opt/python")

# Import MCP components

# Import AlphaVantage MCP server components
from alphavantage_mcp_server.server import (
    handle_list_tools,
    handle_call_tool,
    list_prompts,
    get_prompt,
    get_version,
)
from alphavantage_mcp_server.oauth import (
    OAuthResourceServer,
    create_oauth_config_from_env,
)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for stateless MCP requests.
    Each request is handled independently without session state.
    """
    try:
        # Parse the incoming request
        if "body" not in event:
            return create_error_response(400, "Missing request body")

        # Handle both string and already-parsed JSON bodies
        if isinstance(event["body"], str):
            try:
                request_data = json.loads(event["body"])
            except json.JSONDecodeError:
                return create_error_response(400, "Invalid JSON in request body")
        else:
            request_data = event["body"]

        # Validate JSON-RPC format
        if not isinstance(request_data, dict) or "jsonrpc" not in request_data:
            return create_error_response(400, "Invalid JSON-RPC request")

        # Handle OAuth if enabled
        oauth_server = None
        oauth_enabled = os.environ.get("OAUTH_ENABLED", "false").lower() == "true"
        if oauth_enabled:
            oauth_config = create_oauth_config_from_env()
            if oauth_config:
                oauth_server = OAuthResourceServer(oauth_config)

                # Check authentication for non-initialize requests
                method = request_data.get("method", "")
                if method != "initialize":
                    auth_result = validate_oauth_request(event, oauth_server)
                    if not auth_result["authenticated"]:
                        return auth_result["response"]

        # Process the MCP request
        response = asyncio.run(handle_mcp_request(request_data, oauth_server))

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Session-ID",
            },
            "body": json.dumps(response),
        }

    except Exception as e:
        print(f"Lambda handler error: {str(e)}")
        return create_error_response(500, f"Internal server error: {str(e)}")


async def handle_mcp_request(
    request_data: Dict[str, Any], oauth_server: OAuthResourceServer = None
) -> Dict[str, Any]:
    """
    Handle MCP request in stateless mode.
    Each request creates a fresh server instance.
    """
    method = request_data.get("method", "")
    request_id = request_data.get("id", 1)
    params = request_data.get("params", {})

    try:
        # Handle different MCP methods
        if method == "initialize":
            return handle_initialize(request_id, params)

        elif method == "tools/list":
            return await handle_tools_list_request(request_id)

        elif method == "tools/call":
            return await handle_tools_call_request(request_id, params)

        elif method == "prompts/list":
            return await handle_prompts_list_request(request_id)

        elif method == "prompts/get":
            return await handle_prompts_get_request(request_id, params)

        else:
            return create_jsonrpc_error(
                request_id, -32601, f"Method not found: {method}"
            )

    except Exception as e:
        print(f"MCP request error: {str(e)}")
        return create_jsonrpc_error(request_id, -32603, f"Internal error: {str(e)}")


def handle_initialize(request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP initialize request - stateless mode"""
    try:
        version = get_version()
    except Exception:
        version = "0.3.17"  # Fallback version for Lambda

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "experimental": {},
                "prompts": {"listChanged": False},
                "tools": {"listChanged": False},
            },
            "serverInfo": {"name": "alphavantage", "version": version},
        },
    }


async def handle_tools_list_request(request_id: Any) -> Dict[str, Any]:
    """Handle tools/list request - get all available tools"""
    try:
        # Call the AlphaVantage server's handle_list_tools function directly
        tools = await handle_list_tools()

        # Convert MCP Tool objects to JSON-serializable format
        tools_json = []
        for tool in tools:
            tool_dict = {"name": tool.name, "description": tool.description}
            if hasattr(tool, "inputSchema") and tool.inputSchema:
                tool_dict["inputSchema"] = tool.inputSchema
            tools_json.append(tool_dict)

        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools_json}}

    except Exception as e:
        print(f"Tools list error: {str(e)}")
        return create_jsonrpc_error(
            request_id, -32603, f"Failed to list tools: {str(e)}"
        )


async def handle_tools_call_request(
    request_id: Any, params: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle tools/call request - execute a tool"""
    try:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if not tool_name:
            return create_jsonrpc_error(request_id, -32602, "Missing tool name")

        # Call the tool using the AlphaVantage server's handle_call_tool function
        result = await handle_call_tool(tool_name, arguments)

        # Convert MCP result objects to JSON-serializable format
        content_list = []
        if isinstance(result, list):
            for item in result:
                if hasattr(item, "text"):
                    # TextContent object
                    content_list.append({"type": "text", "text": item.text})
                elif hasattr(item, "data"):
                    # ImageContent object
                    content_list.append(
                        {
                            "type": "image",
                            "data": item.data,
                            "mimeType": getattr(item, "mimeType", "image/png"),
                        }
                    )
                elif hasattr(item, "uri"):
                    # EmbeddedResource object
                    content_list.append(
                        {
                            "type": "resource",
                            "resource": {
                                "uri": item.uri,
                                "text": getattr(item, "text", ""),
                                "mimeType": getattr(item, "mimeType", "text/plain"),
                            },
                        }
                    )
                else:
                    # Fallback for unknown types
                    content_list.append({"type": "text", "text": str(item)})
        else:
            # Single result
            if hasattr(result, "text"):
                content_list.append({"type": "text", "text": result.text})
            else:
                content_list.append({"type": "text", "text": str(result)})

        return {"jsonrpc": "2.0", "id": request_id, "result": {"content": content_list}}

    except Exception as e:
        print(f"Tool call error: {str(e)}")
        return create_jsonrpc_error(
            request_id, -32603, f"Tool execution failed: {str(e)}"
        )


async def handle_prompts_list_request(request_id: Any) -> Dict[str, Any]:
    """Handle prompts/list request"""
    try:
        # Call the AlphaVantage server's list_prompts function directly
        prompts = await list_prompts()

        # Convert to JSON-serializable format
        prompts_json = []
        for prompt in prompts:
            prompt_dict = {"name": prompt.name, "description": prompt.description}
            if hasattr(prompt, "arguments") and prompt.arguments:
                prompt_dict["arguments"] = prompt.arguments
            prompts_json.append(prompt_dict)

        return {"jsonrpc": "2.0", "id": request_id, "result": {"prompts": prompts_json}}

    except Exception as e:
        print(f"Prompts list error: {str(e)}")
        return create_jsonrpc_error(
            request_id, -32603, f"Failed to list prompts: {str(e)}"
        )


async def handle_prompts_get_request(
    request_id: Any, params: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle prompts/get request"""
    try:
        prompt_name = params.get("name")
        arguments = params.get("arguments", {})

        if not prompt_name:
            return create_jsonrpc_error(request_id, -32602, "Missing prompt name")

        # Call the prompt using the AlphaVantage server's get_prompt function
        result = await get_prompt(prompt_name, arguments)

        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    except Exception as e:
        print(f"Prompt get error: {str(e)}")
        return create_jsonrpc_error(
            request_id, -32603, f"Failed to get prompt: {str(e)}"
        )


def validate_oauth_request(
    event: Dict[str, Any], oauth_server: OAuthResourceServer
) -> Dict[str, Any]:
    """Validate OAuth authentication for the request"""
    try:
        # Extract authorization header
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization") or headers.get("authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return {
                "authenticated": False,
                "response": create_oauth_error_response(
                    401, "invalid_token", "Missing or invalid authorization header"
                ),
            }

        # TODO: Implement OAuth token validation using oauth_server
        # For now, return authenticated=True to allow requests
        return {"authenticated": True}

    except Exception as e:
        return {
            "authenticated": False,
            "response": create_oauth_error_response(
                500, "server_error", f"OAuth validation error: {str(e)}"
            ),
        }


def create_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """Create a standard error response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"error": {"code": status_code, "message": message}}),
    }


def create_jsonrpc_error(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    """Create a JSON-RPC error response"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def create_oauth_error_response(
    status_code: int, error_type: str, description: str
) -> Dict[str, Any]:
    """Create an OAuth error response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "WWW-Authenticate": f'Bearer error="{error_type}", error_description="{description}"',
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"error": error_type, "error_description": description}),
    }

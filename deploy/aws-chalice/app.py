import asyncio
import os

from chalice import Chalice, Response
from chalice.app import Request
from mcp.server.streamable_http import StreamableHTTPServerTransport
from starlette.requests import Request as StarletteRequest

# Import the MCP server components
from alphavantage_mcp_server.oauth import OAuthResourceServer, create_oauth_config_from_env

app = Chalice(app_name='alphavantage-mcp-server')

# Global variables for server components
transport = None
oauth_server: OAuthResourceServer = None


def sync_wrapper(async_func, *args, **kwargs):
    """Global sync wrapper for async functions to avoid Chalice serialization issues"""
    return asyncio.run(async_func(*args, **kwargs))


def initialize_server():
    """Initialize the MCP server components"""
    global transport, oauth_server

    if transport is None:
        transport = StreamableHTTPServerTransport(
            mcp_session_id=None,
            is_json_response_enabled=True
        )
    
    # Initialize OAuth if enabled (works with any OAuth 2.0 server including Cognito)
    oauth_enabled = os.getenv('OAUTH_ENABLED', 'false').lower() == 'true'
    if oauth_enabled and oauth_server is None:
        oauth_config = create_oauth_config_from_env()
        if oauth_config:
            oauth_server = OAuthResourceServer(oauth_config)


async def handle_mcp_request(chalice_request: Request) -> Response:
    """Handle MCP requests through the existing server logic"""
    initialize_server()
    
    # Convert Chalice request to ASGI scope format
    # Note: Chalice Request object has different attributes than expected
    query_params = getattr(chalice_request, 'query_params', {}) or {}
    query_string = "&".join([f"{k}={v}" for k, v in query_params.items()]).encode() if query_params else b""
    
    scope = {
        "type": "http",
        "method": chalice_request.method,
        "path": chalice_request.path,
        "query_string": query_string,
        "headers": [
            [key.lower().encode(), value.encode()] 
            for key, value in (chalice_request.headers or {}).items()
        ],
    }
    
    # Create receive callable for request body
    # Handle different ways Chalice might provide the body
    body = b""
    if hasattr(chalice_request, 'raw_body') and chalice_request.raw_body:
        body = chalice_request.raw_body
    elif hasattr(chalice_request, 'json_body') and chalice_request.json_body:
        import json
        body = json.dumps(chalice_request.json_body).encode()
    elif hasattr(chalice_request, 'body') and chalice_request.body:
        body = chalice_request.body if isinstance(chalice_request.body, bytes) else chalice_request.body.encode()
    
    async def receive():
        return {
            "type": "http.request",
            "body": body,
            "more_body": False,
        }
    
    # Create send callable to capture response
    response_data = {}
    
    async def send(message):
        if message["type"] == "http.response.start":
            response_data["status"] = message["status"]
            response_data["headers"] = {
                key.decode(): value.decode() 
                for key, value in message.get("headers", [])
            }
        elif message["type"] == "http.response.body":
            response_data["body"] = message.get("body", b"")
    
    # Handle OAuth metadata endpoint if OAuth is enabled
    if oauth_server and chalice_request.path == oauth_server.config.resource_metadata_path:
        starlette_request = StarletteRequest(scope, receive)
        starlette_response = await oauth_server.handle_resource_metadata_request(starlette_request)
        
        return Response(
            body=starlette_response.body,
            status_code=starlette_response.status_code,
            headers=dict(starlette_response.headers)
        )
    
    # Handle MCP requests
    elif chalice_request.path.startswith("/mcp"):
        # OAuth authentication if enabled
        if oauth_server:
            starlette_request = StarletteRequest(scope, receive)
            session_id = chalice_request.headers.get("X-Session-ID")
            
            is_authenticated, validation_result = await oauth_server.authenticate_request(
                starlette_request, session_id
            )
            
            if not is_authenticated:
                if validation_result and validation_result.error == "Insufficient scopes":
                    error_response = await oauth_server.create_forbidden_response(
                        error="insufficient_scope",
                        description="Required scopes not present in token"
                    )
                else:
                    error_desc = validation_result.error if validation_result else "No valid token provided"
                    error_response = await oauth_server.create_unauthorized_response(
                        error="invalid_token",
                        description=error_desc
                    )
                
                return Response(
                    body=error_response.body,
                    status_code=error_response.status_code,
                    headers=dict(error_response.headers)
                )
        
        # Process MCP request
        try:
            await transport.handle_request(scope, receive, send)

            return Response(
                body=response_data.get("body", b""),
                status_code=response_data.get("status", 200),
                headers=response_data.get("headers", {})
            )
        except Exception as e:
            return Response(
                body=f"Internal Server Error: {str(e)}",
                status_code=500,
                headers={"content-type": "text/plain"}
            )
    
    # Return 404 for unknown paths
    return Response(
        body="Not Found",
        status_code=404,
        headers={"content-type": "text/plain"}
    )


@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return {
        "service": "AlphaVantage MCP Server",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.route('/.well-known/oauth-protected-resource', methods=['GET'])
def oauth_metadata():
    """OAuth 2.0 Protected Resource Metadata endpoint"""
    return sync_wrapper(handle_mcp_request, app.current_request)


@app.route('/mcp/{proxy+}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def mcp_proxy(proxy):
    """Handle all MCP requests"""
    return sync_wrapper(handle_mcp_request, app.current_request)


@app.route('/mcp', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def mcp_root():
    """Handle MCP root requests"""
    return sync_wrapper(handle_mcp_request, app.current_request)


# Error handlers
@app.middleware('http')
def add_cors_headers(event, get_response):
    """Add CORS headers for browser compatibility"""
    response = get_response(event)
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Session-ID',
    })
    return response


@app.middleware('http')
def handle_preflight(event, get_response):
    """Handle CORS preflight requests"""
    if event.method == 'OPTIONS':
        return Response(
            body='',
            status_code=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Session-ID',
            }
        )
    return get_response(event)

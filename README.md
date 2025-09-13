# ✅ Official Alpha Vantage MCP Server

[![smithery badge](https://smithery.ai/badge/@calvernaz/alphavantage)](https://smithery.ai/server/@calvernaz/alphavantage)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/b76d0966-edd1-46fd-9cfb-b29a6d8cb563)

A MCP server for the stock market data API, Alphavantage API.

**MCP Server URL**: https://mcp.alphavantage.co

## Configuration

### Getting an API Key
1. Sign up for a [Free Alphavantage API key](https://www.alphavantage.co/support/#api-key)
2. Add the API key to your environment variables as `ALPHAVANTAGE_API_KEY`


## Installation

### Option 1: Using uvx (Recommended)

The easiest way to use the AlphaVantage MCP server is with `uvx`:

```bash
# Run directly without installation
uvx alphavantage-mcp

# Or with specific arguments
uvx alphavantage-mcp --server http --port 8080
```

### Option 2: Using pip

```bash
pip install alphavantage-mcp
alphavantage-mcp
```

### Option 3: From source

```bash
git clone https://github.com/calvernaz/alphavantage.git
cd alphavantage
uv run alphavantage
```

## Server Modes

The AlphaVantage server can run in two different modes:

### Stdio Server (Default)
This is the standard MCP server mode used for tools like Claude Desktop.

```bash
alphavantage
# or explicitly:
alphavantage --server stdio
```

### Streamable HTTP Server
This mode provides real-time updates via HTTP streaming.

```bash
alphavantage --server http --port 8080
```

### Streamable HTTP Server with OAuth 2.1 Authentication
This mode adds OAuth 2.1 authentication to the HTTP server, following the MCP specification for secure access.

```bash
alphavantage --server http --port 8080 --oauth
```

#### OAuth Configuration

When using the `--oauth` flag, the server requires OAuth 2.1 configuration via environment variables:

**Required Environment Variables:**
```bash
export OAUTH_AUTHORIZATION_SERVER_URL="https://your-auth-server.com/realms/your-realm"
export OAUTH_RESOURCE_SERVER_URI="https://your-mcp-server.com"
```

**Optional Environment Variables:**
```bash
# Token validation method (default: jwt)
export OAUTH_TOKEN_VALIDATION_METHOD="jwt"  # or "introspection"

# For JWT validation
export OAUTH_JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
export OAUTH_JWT_ALGORITHM="RS256"  # default

# For token introspection validation
export OAUTH_INTROSPECTION_ENDPOINT="https://your-auth-server.com/realms/your-realm/protocol/openid-connect/token/introspect"
export OAUTH_INTROSPECTION_CLIENT_ID="your-client-id"
export OAUTH_INTROSPECTION_CLIENT_SECRET="your-client-secret"

# Optional: Required scopes (space-separated)
export OAUTH_REQUIRED_SCOPES="mcp:access mcp:read"

# Optional: Enable session binding for additional security (default: true)
export OAUTH_SESSION_BINDING_ENABLED="true"
```

#### OAuth Features

The OAuth implementation provides:

- **OAuth 2.0 Protected Resource Metadata** endpoint (`/.well-known/oauth-protected-resource`)
- **Bearer token authentication** for all MCP requests
- **JWT and Token Introspection** validation methods
- **MCP Security Best Practices** compliance:
  - Token audience validation (prevents token passthrough attacks)
  - Session hijacking prevention with secure session IDs
  - User-bound sessions for additional security
  - Proper WWW-Authenticate headers for 401 responses

#### Example: Keycloak Configuration

For testing with Keycloak:

```bash
# Keycloak OAuth configuration
export OAUTH_AUTHORIZATION_SERVER_URL="https://keycloak.example.com/realms/mcp-realm"
export OAUTH_RESOURCE_SERVER_URI="https://mcp.example.com"
export OAUTH_TOKEN_VALIDATION_METHOD="introspection"
export OAUTH_INTROSPECTION_ENDPOINT="https://keycloak.example.com/realms/mcp-realm/protocol/openid-connect/token/introspect"
export OAUTH_INTROSPECTION_CLIENT_ID="mcp-server"
export OAUTH_INTROSPECTION_CLIENT_SECRET="your-keycloak-client-secret"
export OAUTH_REQUIRED_SCOPES="mcp:access"

# Start server with OAuth
alphavantage --server http --port 8080 --oauth
```

#### OAuth Client Flow

When OAuth is enabled, MCP clients must:

1. **Discover** the authorization server via `GET /.well-known/oauth-protected-resource`
2. **Register** with the authorization server (if using Dynamic Client Registration)
3. **Obtain access tokens** from the authorization server
4. **Include tokens** in requests: `Authorization: Bearer <access-token>`
5. **Handle 401/403 responses** and refresh tokens as needed

Options:
- `--server`: Choose between `stdio` (default) or `http` server mode
- `--port`: Specify the port for the Streamable HTTP server (default: 8080)
- `--oauth`: Enable OAuth 2.1 authentication (requires `--server http`)

## 📊 Telemetry

The AlphaVantage MCP server includes optional Prometheus metrics for monitoring and observability.

### Enabling Telemetry

Set the following environment variables to enable telemetry:

```bash
# Enable telemetry (default: true)
export MCP_TELEMETRY_ENABLED=true

# Server identification (optional)
export MCP_SERVER_NAME=alphavantage
export MCP_SERVER_VERSION=1.0.0

# Metrics server port (default: 9464)
export MCP_METRICS_PORT=9464
```

### Metrics Endpoint

When telemetry is enabled, Prometheus metrics are available at:

```
http://localhost:9464/metrics
```

### Available Metrics

The server collects the following metrics for each tool call:

- **`mcp_tool_calls_total`** - Total number of tool calls (labeled by tool and outcome)
- **`mcp_tool_latency_seconds`** - Tool execution latency histogram
- **`mcp_tool_request_bytes`** - Request payload size histogram
- **`mcp_tool_response_bytes`** - Response payload size histogram
- **`mcp_tool_active_concurrency`** - Active concurrent tool calls gauge
- **`mcp_tool_errors_total`** - Total errors by type (timeout, bad_input, connection, unknown)

### Example Usage with Telemetry

```bash
# Start server with telemetry enabled
export MCP_TELEMETRY_ENABLED=true
export MCP_SERVER_NAME=alphavantage-prod
export ALPHAVANTAGE_API_KEY=your_api_key
alphavantage --server http --port 8080

# View metrics
curl http://localhost:9464/metrics
```

## 🚀 AWS Serverless Deployment

Deploy the AlphaVantage MCP Server on AWS Lambda using the stateless MCP pattern for production-ready, scalable deployment.

### Quick AWS Deployment

```bash
cd deploy/aws-stateless-mcp-lambda
export ALPHAVANTAGE_API_KEY=your_api_key_here
./deploy.sh
```

**Features:**
- ✅ **Stateless MCP pattern** - Perfect for Lambda's execution model
- ✅ **Auto-scaling** - Handles any load with AWS Lambda + API Gateway
- ✅ **Cost-effective** - Pay only for requests (~$1-5/month for typical usage)
- ✅ **Production-ready** - Based on AWS official sample patterns
- ✅ **OAuth 2.1 support** - Optional authentication for secure access

**📖 Full Documentation:** See [AWS Deployment Guide](deploy/aws-stateless-mcp-lambda/README.md) for complete setup instructions, testing, monitoring, and troubleshooting.

### Usage with Claude Desktop

#### Option 1: Using uvx (Recommended)
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "alphavantage": {
      "command": "uvx",
      "args": ["alphavantage-mcp"],
      "env": {
        "ALPHAVANTAGE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

#### Option 2: From source
If you cloned the repository, use this configuration:

```json
{
  "mcpServers": {
    "alphavantage": {
      "command": "uv",
      "args": [
        "--directory",
        "<DIRECTORY-OF-CLONED-PROJECT>/alphavantage",
        "run",
        "alphavantage"
      ],
      "env": {
        "ALPHAVANTAGE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```
#### Running the Server in Streamable HTTP Mode

**Using uvx:**
```json
{
  "mcpServers": {
    "alphavantage": {
      "command": "uvx",
      "args": ["alphavantage-mcp", "--server", "http", "--port", "8080"],
      "env": {
        "ALPHAVANTAGE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**From source:**
```json
{
  "mcpServers": {
    "alphavantage": {
      "command": "uv",
      "args": [
        "--directory",
        "<DIRECTORY-OF-CLONED-PROJECT>/alphavantage",
        "run",
        "alphavantage",
        "--server",
        "http",
        "--port",
        "8080"
      ],
      "env": {
        "ALPHAVANTAGE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```


## 📺 Demo Video

Watch a quick demonstration of the Alpha Vantage MCP Server in action:

[![Alpha Vantage MCP Server Demo](https://github.com/user-attachments/assets/bc9ecffb-eab6-4a4d-bbf6-9fc8178f15c3)](https://github.com/user-attachments/assets/bc9ecffb-eab6-4a4d-bbf6-9fc8178f15c3)


## 🔧 Development & Publishing

### Publishing to PyPI

This project includes scripts for publishing to PyPI and TestPyPI:

```bash
# Publish to TestPyPI (for testing)
python scripts/publish.py --test

# Publish to PyPI (production)
python scripts/publish.py

# Use uv publish instead of twine
python scripts/publish.py --test --use-uv
```

The script uses `twine` by default (recommended) but can also use `uv publish` with the `--use-uv` flag.

### GitHub Actions

The repository includes a GitHub Actions workflow for automated publishing:

- **Trusted Publishing**: Uses PyPA's official publish action with OpenID Connect
- **Manual Trigger**: Can be triggered manually with options for TestPyPI vs PyPI
- **Twine Fallback**: Supports both trusted publishing and twine-based publishing

To set up publishing:

1. **For Trusted Publishing** (recommended):
   - Configure trusted publishing on PyPI/TestPyPI with your GitHub repository
   - No secrets needed - uses OpenID Connect

2. **For Token-based Publishing**:
   - Add `PYPI_API_TOKEN` and `TEST_PYPI_API_TOKEN` secrets to your repository
   - Use the "Use twine" option in the workflow dispatch

## 🤝 Contributing

We welcome contributions from the community! To get started, check out our [contribution](CONTRIBUTING.md) guide for setup instructions,
development tips, and guidelines.

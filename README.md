# ✅ Official Alpha Vantage MCP Server

[![smithery badge](https://smithery.ai/badge/@calvernaz/alphavantage)](https://smithery.ai/server/@calvernaz/alphavantage)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/b76d0966-edd1-46fd-9cfb-b29a6d8cb563)

A MCP server for the stock market data API, Alphavantage API.

**MCP Server URL**: https://mcp.alphavantage.co

## Configuration

### Getting an API Key
1. Sign up for a [Free Alphavantage API key](https://www.alphavantage.co/support/#api-key)
2. Add the API key to your environment variables as `ALPHAVANTAGE_API_KEY`


## Clone the project

```bash
git clone https://github.com/calvernaz/alphavantage.git
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

### Usage with Claude Desktop
Add this to your `claude_desktop_config.json`:

**NOTE** Make sure you replace the `<DIRECTORY-OF-CLONED-PROJECT>` with the directory of the cloned project.

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
### Running the Server in Streamable HTTP Mode

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


## 🤝 Contributing

We welcome contributions from the community! To get started, check out our [contribution](CONTRIBUTING.md) guide for setup instructions, 
development tips, and guidelines.

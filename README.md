# ✅ Official Alpha Vantage MCP Server

[![smithery badge](https://smithery.ai/badge/@calvernaz/alphavantage)](https://smithery.ai/server/@calvernaz/alphavantage)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/b76d0966-edd1-46fd-9cfb-b29a6d8cb563)

A MCP server for the stock market data API, Alphavantage API. 

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

### SSE (Server-Sent Events) Server
This mode provides real-time updates via HTTP streaming.

```bash
alphavantage --server sse --port 8080
```

Options:
- `--server`: Choose between `stdio` (default) or `sse` server mode
- `--port`: Specify the port for the SSE server (default: 8080)

### Usage with Claude Desktop
Add this to your `claude_desktop_config.json`:

**NOTE** Make sure you replace the `<DIRECTORY-OF-CLONED-PROJECT>` with the directory of the cloned project.

```
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

## 📺 Demo Video

Watch a quick demonstration of the Alpha Vantage MCP Server in action:

[![Alpha Vantage MCP Server Demo](https://github.com/user-attachments/assets/bc9ecffb-eab6-4a4d-bbf6-9fc8178f15c3)](https://github.com/user-attachments/assets/bc9ecffb-eab6-4a4d-bbf6-9fc8178f15c3)


## 🤝 Contributing

We welcome contributions from the community! To get started, check out our [contribution](CONTRIBUTING.md) guide for setup instructions, 
development tips, and guidelines.

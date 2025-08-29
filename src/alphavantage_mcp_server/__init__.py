import asyncio
import argparse
import os
from . import server


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='AlphaVantage MCP Server')
    parser.add_argument('--server', type=str, choices=['stdio', 'http'],
                       help='Server type: stdio or http (default: stdio, or from TRANSPORT env var)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Port for HTTP server (default: 8080)')
    parser.add_argument('--oauth', action='store_true',
                       help='Enable OAuth 2.1 authentication for HTTP server (requires --server http)')

    args = parser.parse_args()
    
    # Determine server type: command line arg takes precedence, then env var, then default to stdio
    server_type = args.server
    if server_type is None:
        transport_env = os.getenv('TRANSPORT', '').lower()
        if transport_env == 'http':
            server_type = 'http'
        else:
            server_type = 'stdio'

    # Validate OAuth flag usage
    if args.oauth and server_type != 'http':
        parser.error("--oauth flag can only be used with --server http or TRANSPORT=http")

    # Use the patched server.main function directly
    asyncio.run(server.main(server_type=server_type, port=args.port, oauth_enabled=args.oauth))


if __name__ == '__main__':
    main()


__all__ = ["main", "server"]

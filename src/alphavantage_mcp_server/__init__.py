import asyncio
import argparse
from . import server


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='AlphaVantage MCP Server')
    parser.add_argument('--server', type=str, choices=['stdio', 'http'], default='stdio',
                       help='Server type: stdio or http (default: stdio)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Port for HTTP server (default: 8080)')
    parser.add_argument('--oauth', action='store_true',
                       help='Enable OAuth 2.1 authentication for HTTP server (requires --server http)')

    args = parser.parse_args()
    
    # Validate OAuth flag usage
    if args.oauth and args.server != 'http':
        parser.error("--oauth flag can only be used with --server http")
    
    # Use the patched server.main function directly
    asyncio.run(server.main(server_type=args.server, port=args.port, oauth_enabled=args.oauth))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Alpha Vantage MCP Server')
    parser.add_argument('--server', type=str, choices=['stdio', 'http'], default='stdio',
                        help='Server type: stdio or http (default: stdio)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port for HTTP server (default: 8080)')
    parser.add_argument('--oauth', action='store_true',
                        help='Enable OAuth 2.1 authentication for HTTP server (requires --server http)')

    args = parser.parse_args()
    
    # Validate OAuth flag usage
    if args.oauth and args.server != 'http':
        parser.error("--oauth flag can only be used with --server http")
    
    # Use the patched server.main function directly
    asyncio.run(server.main(server_type=args.server, port=args.port, oauth_enabled=args.oauth))


__all__ = ["main", "server"]

import asyncio
import argparse
from . import server


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='AlphaVantage MCP Server')
    parser.add_argument('--server', type=str, choices=['stdio', 'sse'], default='stdio',
                       help='Server type: stdio or sse (default: stdio)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Port for SSE server (default: 8080)')

    args = parser.parse_args()
    asyncio.run(server.main(server_type=args.server, port=args.port))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Alpha Vantage MCP Server')
    parser.add_argument('--server', type=str, choices=['stdio', 'sse'], default='stdio',
                        help='Server type: stdio or sse (default: stdio)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port for SSE server (default: 8080)')

    args = parser.parse_args()
    asyncio.run(server.main(server_type=args.server, port=args.port))


__all__ = ["main", "server"]

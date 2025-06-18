"""
Freepik FastMCP Server - Main Entry Point

A professionally structured MCP server for Freepik API integration.
Built with Domain-Driven Design principles for maintainability and clarity.
"""

from src.application.server_factory import ServerFactory

# Create the server instance using factory pattern
# This needs to be a module-level variable for FastMCP to find it
try:
    print("🚀 Initializing Freepik FastMCP Server...")
    mcp = ServerFactory.create_server()
    print("✅ Server factory initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize server: {e}")
    raise


def main() -> None:
    """Main entry point for the Freepik FastMCP server."""
    try:
        print("🔌 Ready to accept MCP connections")

        # Run the server
        mcp.run(transport="stdio")

    except Exception as e:
        print(f"❌ Failed to run server: {e}")
        raise


if __name__ == "__main__":
    main()

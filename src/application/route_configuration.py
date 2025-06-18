"""
Route configuration for MCP server.
"""

from fastmcp.server.openapi import MCPType, RouteMap


class RouteConfiguration:
    """Manages route mapping configuration for the MCP server."""

    @staticmethod
    def get_route_maps() -> list[RouteMap]:
        """
        Get the route maps configuration for the MCP server.

        This configuration defines which API endpoints are exposed and how they're mapped:
        - Icons API: Full access to icon search and download functionality
        - Resources API: Full access to resource management
        - AI Classifier: Image classification capabilities
        - Mystic AI: Advanced AI features (when available)
        - All other routes are excluded for security and simplicity

        Returns:
            List of RouteMap objects defining the server's route configuration.
        """
        return [
            # Icons API - Full access
            RouteMap(
                methods=[
                    "GET",
                    "POST",
                ],
                pattern=r"/v1/icon.*",
                mcp_type=MCPType.TOOL,
            ),
            # Resources API - Full access
            RouteMap(
                methods=[
                    "GET",
                    "POST",
                ],
                pattern=r"/v1/resource.*",
                mcp_type=MCPType.TOOL,
            ),
            # AI Image Classifier - Specific endpoint
            RouteMap(
                methods=[
                    "POST",
                ],
                pattern=r"/v1/ai/classifier/image$",
                mcp_type=MCPType.TOOL,
            ),
            # Mystic AI - Advanced AI features
            RouteMap(
                methods=[
                    "POST",
                ],
                pattern=r"/v1/ai/mystic.*",
                mcp_type=MCPType.TOOL,
            ),
            # Exclude all other routes for security and simplicity
            RouteMap(
                methods=[
                    "GET",
                    "POST",
                ],
                pattern=r".*",
                mcp_type=MCPType.EXCLUDE,
            ),
        ]

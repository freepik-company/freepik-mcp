"""
Server factory for creating and configuring the MCP server.
"""

from typing import Any

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context
from fastmcp.server.openapi import OpenAPITool
from fastmcp.tools import Tool

from ..domain.config import ApiConfig, CacheConfig, ServerConfig
from ..infrastructure.http_client import HttpClientFactory
from ..infrastructure.mystic_service import MysticService
from ..infrastructure.openapi_loader import OpenApiSpecLoader
from .route_configuration import RouteConfiguration


class ServerFactory:
    """Factory for creating and configuring the FastMCP server."""

    @staticmethod
    def create_server() -> FastMCP[Any]:
        """
        Create a fully configured FastMCP server.

        This factory method handles the complete setup process:
        1. Load configuration from environment
        2. Create HTTP client with authentication (now dynamic per request)
        3. Load OpenAPI specification with caching
        4. Configure route mappings
        5. Create and return the configured server

        Returns:
            Fully configured FastMCP server ready to run.

        Raises:
            ValueError: If required configuration is missing.
            Exception: If unable to load OpenAPI specification.
        """
        # Load configurations
        api_config = ApiConfig.from_environment()
        cache_config = CacheConfig()
        server_config = ServerConfig()

        # Create HTTP client for initial server setup (will be replaced by dynamic clients)
        http_client = HttpClientFactory.create_api_client(api_config)

        # --- Custom AI services handler ---
        ai_service = MysticService()
        transformed_tools = []

        async def mystic_transform_fn(**kwargs: Any) -> dict[str, Any]:
            # Get the active context using the dependency function
            ctx = get_context()
            # kwargs are the POST arguments
            return await ai_service.generate_image_with_polling(kwargs, ctx, timeout=300.0)

        async def kling_transform_fn(**kwargs: Any) -> dict[str, Any]:
            # Get the active context using the dependency function
            ctx = get_context()
            # kwargs are the POST arguments
            return await ai_service.generate_video_with_polling(kwargs, ctx, timeout=600.0)

        def mcp_component_fn(route: Any, component: Any) -> Any:
            # Handle Mystic POST tool
            if (
                route.path == "/v1/ai/mystic"
                and route.method == "POST"
                and isinstance(component, OpenAPITool)
            ):
                # Create a transformed tool
                transformed = Tool.from_tool(
                    component,
                    name="text_to_image_mystic_sync",
                    transform_fn=mystic_transform_fn,
                )
                component.disable()
                transformed_tools.append(transformed)
                return transformed

            # Handle Kling POST tool
            elif (
                route.path == "/v1/ai/image-to-video/kling-std"
                and route.method == "POST"
                and isinstance(component, OpenAPITool)
            ):
                # Create a transformed tool
                transformed = Tool.from_tool(
                    component,
                    name="image_to_video_kling_sync",
                    transform_fn=kling_transform_fn,
                )
                component.disable()
                transformed_tools.append(transformed)
                return transformed

        # Load OpenAPI specification
        spec_loader = OpenApiSpecLoader(cache_config)
        openapi_spec = spec_loader.load_spec()

        # Get route configuration
        route_maps = RouteConfiguration.get_route_maps()

        # Create and configure the server
        server = FastMCP.from_openapi(
            openapi_spec=openapi_spec,
            client=http_client,
            name=server_config.name,
            route_maps=route_maps,
            mcp_component_fn=mcp_component_fn,
        )

        # Explicitly add the transformed tools
        for tool in transformed_tools:
            server.add_tool(tool)

        return server

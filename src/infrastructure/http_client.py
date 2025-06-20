"""
HTTP client factory and configuration.
"""

from typing import Any

import httpx

from ..domain.config import ApiConfig


class HttpClientFactory:
    """Factory for creating HTTP clients with proper configuration."""

    @staticmethod
    def create_api_client(config: ApiConfig) -> httpx.AsyncClient:
        """
        Create an HTTP client configured for the Freepik API.

        Args:
            config: API configuration containing base URL, API key, and timeout.

        Returns:
            Configured HTTP client for Freepik API.
        """
        return httpx.AsyncClient(
            base_url=config.base_url,
            headers={"x-freepik-api-key": config.api_key},
            timeout=config.timeout,
        )

    @staticmethod
    def create_dynamic_client() -> httpx.AsyncClient:
        """
        Create an HTTP client with fresh configuration from environment.
        
        This method reads the current environment configuration each time it's called,
        allowing for dynamic API key updates without server restart.

        Returns:
            Configured HTTP client with current environment settings.
        """
        config = ApiConfig.from_environment()
        
        return httpx.AsyncClient(
            base_url=config.base_url,
            headers={"x-freepik-api-key": config.api_key},
            timeout=config.timeout,
        )

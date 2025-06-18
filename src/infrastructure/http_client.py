"""
HTTP client factory and configuration.
"""

from typing import Any

import httpx
from fastmcp import Context

from ..domain.config import ApiConfig


class ValidatedAsyncClient(httpx.AsyncClient):
    """HTTP client that validates API key on first request."""

    def __init__(self, api_key: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self._validated = False

    async def _validate_if_needed(self, ctx: Context) -> None:
        """Validate API key if not already validated."""
        if not self._validated:
            if self.api_key == "YOUR_API_KEY_HERE" or not self.api_key.strip():
                await ctx.error("❌ No valid FREEPIK_API_KEY configured!")
                await ctx.info("📋 To use Freepik services, please:")
                await ctx.info("   1. Get your API key at: https://freepik.com/api")
                await ctx.info("   2. Set it in your .env file: FREEPIK_API_KEY=your_key_here")
                await ctx.info("   3. Or export it: export FREEPIK_API_KEY=your_key_here")
                await ctx.info("   4. Restart the server after setting the key")
                raise Exception("API key validation failed. Please configure your FREEPIK_API_KEY.")
            self._validated = True


class HttpClientFactory:
    """Factory for creating HTTP clients with proper configuration."""

    @staticmethod
    def create_api_client(config: ApiConfig) -> ValidatedAsyncClient:
        """
        Create an HTTP client configured for the Freepik API.

        Args:
            config: API configuration containing base URL, API key, and timeout.

        Returns:
            Configured HTTP client for Freepik API with lazy validation.
        """
        return ValidatedAsyncClient(
            api_key=config.api_key,
            base_url=config.base_url,
            headers={"x-freepik-api-key": config.api_key},
            timeout=config.timeout,
        )

"""
Domain configuration and value objects.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class ApiConfig:
    """API configuration value object."""

    base_url: str
    api_key: str
    timeout: float = 15.0

    def is_api_key_valid(self) -> bool:
        """Check if the API key is properly configured."""
        return self.api_key != "YOUR_API_KEY_HERE" and bool(self.api_key.strip())

    @classmethod
    def from_environment(cls) -> "ApiConfig":
        """Create API configuration from environment variables."""
        # Load environment variables
        load_dotenv()

        # Get API key from environment
        api_key = os.getenv("FREEPIK_API_KEY")
        if not api_key:
            # Try to load from .env file if not in environment
            env_file = Path(__file__).parent.parent.parent / ".env"
            if env_file.exists():
                load_dotenv(env_file)
                api_key = os.getenv("FREEPIK_API_KEY")

        if not api_key:
            api_key = "YOUR_API_KEY_HERE"  # Placeholder value - will be handled in services

        return cls(base_url="https://api.freepik.com", api_key=api_key, timeout=15.0)


@dataclass(frozen=True)
class CacheConfig:
    """Cache configuration value object."""

    cache_duration_seconds: int = 3600  # 1 hour
    cache_file_name: str = "freepik-openapi-spec.yaml"


@dataclass(frozen=True)
class ServerConfig:
    """Server configuration value object."""

    name: str = "Freepik API Server"
    transport: str = "stdio"

"""
OpenAPI specification loader service.
"""

import tempfile
import time
from pathlib import Path
from typing import Any

import httpx
import yaml

from ..domain.config import CacheConfig


class OpenApiSpecLoader:
    """Service for loading and caching OpenAPI specifications."""

    def __init__(self, cache_config: CacheConfig):
        self._cache_config = cache_config
        self._spec_url = "https://storage.googleapis.com/fc-freepik-pro-rev1-eu-api-specs/freepik-api-v1-openapi.yaml"

    def load_spec(self) -> dict[str, Any]:
        """
        Load OpenAPI spec with caching.

        Returns:
            Dict containing the OpenAPI specification.

        Raises:
            Exception: If unable to load the specification.
        """
        cached_spec = self._load_from_cache()
        if cached_spec is not None:
            return cached_spec

        return self._download_and_cache_spec()

    def _load_from_cache(self) -> dict[str, Any] | None:
        """Load spec from cache if it exists and is recent."""
        cache_file = self._get_cache_file_path()

        if not cache_file.exists():
            return None

        # Check if cache is still valid
        file_age = time.time() - cache_file.stat().st_mtime
        if file_age >= self._cache_config.cache_duration_seconds:
            return None

        print(f"📦 Using cached OpenAPI spec from {cache_file}")
        with open(cache_file, encoding="utf-8") as f:
            loaded_data = yaml.safe_load(f)
            return loaded_data if isinstance(loaded_data, dict) else None

    def _download_and_cache_spec(self) -> dict[str, Any]:
        """Download fresh spec and save to cache."""
        print("🌐 Downloading OpenAPI spec from Freepik...")

        try:
            response = httpx.get(self._spec_url)
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to download OpenAPI spec: {e}")

        # Save to cache
        cache_file = self._get_cache_file_path()
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"💾 Cached OpenAPI spec to {cache_file}")
        loaded_data = yaml.safe_load(response.text)
        if not isinstance(loaded_data, dict):
            raise Exception("Invalid OpenAPI spec format: expected dict")
        return loaded_data

    def _get_cache_file_path(self) -> Path:
        """Get the path to the cache file."""
        temp_dir = Path(tempfile.gettempdir())
        return temp_dir / self._cache_config.cache_file_name

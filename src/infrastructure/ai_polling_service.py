import asyncio
import time
from typing import Any

import httpx
from fastmcp import Context

from .http_client import HttpClientFactory


class AIPollingService:
    """Service for handling AI generation tasks with polling for completion status.

    Supports both Mystic (image generation) and Kling (image-to-video) AI services.
    """

    def __init__(self):
        # No longer store a client instance - we'll create fresh ones per request
        pass

    async def generate_image_with_polling(
        self,
        payload: dict[str, Any],
        ctx: Context,
        poll_interval: float = 5.0,
        timeout: float = 120.0,
    ) -> dict[str, Any]:
        """Generate image using Mystic AI with polling."""
        return await self._generate_with_polling(
            endpoint="/v1/ai/mystic",
            payload=payload,
            ctx=ctx,
            poll_interval=poll_interval,
            timeout=timeout,
            service_name="Mystic"
        )

    async def generate_video_with_polling(
        self,
        payload: dict[str, Any],
        ctx: Context,
        poll_interval: float = 5.0,
        timeout: float = 300.0,
    ) -> dict[str, Any]:
        """Generate video using Kling AI with polling."""
        return await self._generate_with_polling(
            endpoint="/v1/ai/image-to-video/kling",
            payload=payload,
            ctx=ctx,
            poll_interval=poll_interval,
            timeout=timeout,
            service_name="Kling"
        )

    async def _generate_with_polling(
        self,
        endpoint: str,
        payload: dict[str, Any],
        ctx: Context,
        poll_interval: float = 5.0,
        timeout: float = 120.0,
        service_name: str = "AI"
    ) -> dict[str, Any]:
        """Generic method to handle polling for AI generation tasks."""
        start_time = time.time()
        await ctx.info(f"🎨 Starting {service_name.lower()} generation...")

        # Create a fresh client with current configuration for this request
        client = HttpClientFactory.create_dynamic_client()

        try:
            # 1. Make POST request to create the task
            await ctx.debug(f"Sending POST request to {endpoint} with payload: {payload}")
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            ctx.info(f"Response: {data}")
            task_id = data.get("data", {}).get("task_id")
            if not task_id:
                await ctx.error(f"❌ No task_id received from {service_name}")
                raise Exception(f"No task_id received from {service_name}")

            await ctx.info(f"✅ Task created with ID: {task_id}")

            # 2. Poll until it's COMPLETED or fails
            status_url = f"{endpoint}/{task_id}"
            elapsed = 0.0
            poll_count = 0

            while elapsed < timeout:
                await asyncio.sleep(poll_interval)
                elapsed = time.time() - start_time
                poll_count += 1

                await ctx.debug(f"🔍 Query #{poll_count} - Elapsed time: {elapsed:.1f}s")

                # Retry GET up to 3 times if it fails
                status_data = None

                for attempt in range(3):  # 3 attempts maximum
                    try:
                        status_resp = await client.get(status_url)
                        status_resp.raise_for_status()
                        status_data = status_resp.json()
                        break  # If it works, exit the retry loop
                    except Exception as e:
                        if attempt < 2:  # If not the last attempt
                            await ctx.warning(
                                f"⚠️ Error in status query (attempt {attempt + 1}/3): {type(e).__name__}: {str(e)}"
                            )
                            await asyncio.sleep(1)  # Wait 1s before retrying
                        else:
                            await ctx.error(
                                f"❌ Error after 3 attempts querying status: {type(e).__name__}: {str(e)}"
                            )
                            raise Exception(
                                f"Error querying status after 3 attempts: {type(e).__name__}: {str(e)}"
                            )

                if status_data is None:
                    continue  # This shouldn't happen, but for safety

                ai_status = status_data.get("data", {}).get("status")

                await ctx.report_progress(progress=poll_count, total=timeout, message=ai_status)
                await ctx.info(
                    f"📊 Current status: {ai_status} (query #{poll_count}, {elapsed:.1f}s elapsed)"
                )

                if ai_status == "COMPLETED":
                    await ctx.report_progress(progress=100.0, total=100.0)
                    await ctx.info(f"🎉 {service_name} generation completed successfully in {elapsed:.1f} seconds!")
                    result_data = status_data["data"]
                    return result_data if isinstance(result_data, dict) else {}
                if ai_status in ("FAILED", "CANCELLED"):  # other error states
                    await ctx.error(f"❌ {service_name} task failed: {ai_status} after {elapsed:.1f}s")
                    raise Exception(f"{service_name} task failed: {ai_status}")

            await ctx.warning(f"⏰ Timeout after {elapsed:.1f}s waiting for {service_name} to finish")
            raise TimeoutError(f"Timeout waiting for {service_name} to complete the task")

        finally:
            # Always close the client to free resources
            await client.aclose()


# Backward compatibility alias
MysticService = AIPollingService

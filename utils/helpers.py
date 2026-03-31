import random
import asyncio

async def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
    """Wait for a random amount of time to mimic human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)

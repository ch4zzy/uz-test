from redis import asyncio as aioredis

from app.dependencies import REDIS_URL

redis = aioredis.from_url(REDIS_URL)

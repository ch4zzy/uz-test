import asyncio
from contextlib import asynccontextmanager

import asyncpg


class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        retries = 5
        for attempt in range(retries):
            try:
                self.pool = await asyncpg.create_pool(self.database_url)
                break
            except Exception as e:
                if attempt < retries - 1:
                    print(f"Connection attempt {attempt + 1} failed: {e}. Retrying in 2 seconds...")
                    await asyncio.sleep(2)
                else:
                    raise

    async def disconnect(self):
        await self.pool.close()

    @asynccontextmanager
    async def get_connection(self):
        async with self.pool.acquire() as connection:
            yield connection

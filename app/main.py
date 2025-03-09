from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.routes import stations, trains, trips
from app.dependencies import db, stations_repo, trains_repo, trips_repo
from app.redis import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await stations_repo.create_table()
    await trains_repo.create_table()
    await trips_repo.create_table()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

# Include the routers
app.include_router(stations.router)
app.include_router(trains.router)
app.include_router(trips.router)

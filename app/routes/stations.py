from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.dependencies import stations_repo
from app.models import Station

router = APIRouter(prefix="/station", tags=["stations"])


@router.get("/list", status_code=200)
@cache(expire=60)
async def get_station_list():
    station_list = await stations_repo.list()
    context = [
        {
            "id": station.id,
            "name": station.name,
            "code": station.code
        } for station in station_list]

    return context


@router.get("/{code}", status_code=200)
@cache(expire=60)
async def get_station(code: int):
    station = await stations_repo.get(code)
    context = {"name": station.name}
    return context


@router.post("", status_code=201)
async def create_station(station: Station):
    station = await stations_repo.create(station)
    context = {"name": station.name, "code": station.code}
    return context

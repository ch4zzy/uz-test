from datetime import datetime

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.dependencies import trips_repo
from app.models import Trip

router = APIRouter(prefix="/trip", tags=["trips"])


@router.post("", status_code=201)
async def create_trip(trip: Trip):
    trip = await trips_repo.create(trip)
    context = {
        "train_number": trip.train_number,
        "departure_station_code": trip.departure_station_code,
        "arrival_station_code": trip.arrival_station_code,
        "departure_time": trip.departure_time,
        "arrival_time": trip.arrival_time
    }
    return context


@router.get("/list", status_code=200)
@cache(expire=60)
async def get_trip_list(
        departure_station_code: int = Query(..., example=2200001),
        arrival_station_code: int = Query(..., example=2200002),
        departure_time: datetime = Query(..., example="2023-04-09T14:07:13.672Z"),
        arrival_time: datetime = Query(..., example="2026-04-09T14:07:13.672Z")
):
    trips_list = await trips_repo.list(
        departure_station_code,
        arrival_station_code,
        departure_time,
        arrival_time
    )
    return trips_list

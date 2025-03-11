from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.dependencies import trains_repo
from app.models import Train, Wagon
from app.utils import normalize_wagons

router = APIRouter(prefix="/train", tags=["trains"])


@router.get("/{number}", status_code=200)
@cache(expire=60)
async def get_train(number: str):
    train = await trains_repo.get(number)
    wagons = [wagon.number for wagon in train.wagons]
    context = {"number": train.number, "wagons": wagons}
    return context


@router.post("", status_code=201)
async def create_train(train: Train):
    renumbered_wagons = await normalize_wagons(train)
    train = await trains_repo.create(train.number, renumbered_wagons)
    context = {"number": train.number, "wagons": [wagon.number for wagon in train.wagons]}
    return context


@router.patch("/{number}", status_code=200)
async def update_train_wagons(number: str, wagons: list[Wagon]):
    train = await trains_repo.get(number)
    renumbered_wagons = await normalize_wagons(Train(number=number, wagons=wagons))
    train = await trains_repo.update(number, renumbered_wagons)
    context = {"number": train.number, "wagons": [wagon.number for wagon in train.wagons]}
    return context

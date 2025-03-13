import os
from app.database import Database
from app.repository import StationRepository, TrainRepository, TripRepository

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

REDIS_URL = os.environ.get("REDIS_URL")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

db = Database(DATABASE_URL)
stations_repo = StationRepository(db)
trains_repo = TrainRepository(db)
trips_repo = TripRepository(db)

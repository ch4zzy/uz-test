import asyncpg
import json
from typing import List
from fastapi import HTTPException
from datetime import datetime
from app.models import Station, Wagon, Train, Trip
from app.dependencies import Database


class StationRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create_table(self) -> None:
        async with self.db.get_connection() as connection:
            await connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS stations 
                (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) NOT NULL,
                    code INT NOT NULL CHECK 
                    (code >= 2200000 AND code <= 2299999) UNIQUE
                )
                '''
            )

    async def list(self) -> List[Station]:
        async with self.db.get_connection() as connection:
            rows = await connection.fetch(
                '''
                SELECT name, code FROM stations
                '''
            )
            return [Station(**row) for row in rows] if rows else []

    async def get(self, code: int) -> Station:
        async with self.db.get_connection() as connection:
            row = await connection.fetchrow(
                '''
                SELECT name, code FROM stations WHERE code = $1
                ''', code
            )
            if not row:
                raise HTTPException(status_code=404, detail="Station not found")
            return Station(**row) if row else None

    async def create(self, station: Station) -> Station:
        async with self.db.get_connection() as connection:
            try:
                await connection.execute(
                    '''
                    INSERT INTO stations (name, code) VALUES ($1, $2)
                    ''', station.name, station.code
                )
                return await self.get(station.code)
            except asyncpg.exceptions.UniqueViolationError:
                raise HTTPException(status_code=400, detail="Station with this code already exists")


class TrainRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create_table(self) -> None:
        async with self.db.get_connection() as connection:
            await connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS trains 
                (
                    id SERIAL PRIMARY KEY,
                    number VARCHAR(4) NOT NULL UNIQUE,
                    wagons JSONB NOT NULL 
                    CHECK (jsonb_typeof(wagons) = 'array')
                )
                '''
            )

    async def get(self, number: str) -> Train:
        async with self.db.get_connection() as connection:
            row = await connection.fetchrow(
                '''
                SELECT number, wagons FROM trains WHERE number = $1
                ''', number
            )
            if not row:
                raise HTTPException(status_code=404, detail="Train not found")
            wagons_data = json.loads(row['wagons'])
            wagons = [Wagon(number=w) for w in wagons_data]
            return Train(number=row['number'], wagons=wagons)

    async def create(self, number: str, wagons: List[str]) -> Train:
        async with self.db.get_connection() as connection:
            try:
                await connection.execute(
                    '''
                    INSERT INTO trains (number, wagons) VALUES ($1, $2)
                    ''', number, json.dumps(wagons))
                return await self.get(number)
            except asyncpg.exceptions.UniqueViolationError:
                raise HTTPException(status_code=400, detail="Train with this number already exists")

    async def update(self, number: str, wagons: List[str]) -> Train:
        async with self.db.get_connection() as connection:
            try:
                row = await connection.fetchrow(
                    '''
                    UPDATE trains SET wagons = $2 WHERE number = $1 RETURNING id, number, wagons
                    ''', number, json.dumps(wagons)
                )
                if not row:
                    raise HTTPException(status_code=404, detail="Train not found")
                wagons_data = json.loads(row['wagons'])
                wagons = [Wagon(number=w) for w in wagons_data]
                return Train(number=row['number'], wagons=wagons)
            except asyncpg.exceptions.UniqueViolationError:
                raise HTTPException(status_code=400, detail="Train update failed due to unique violation")


class TripRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create_table(self) -> None:
        async with self.db.get_connection() as connection:
            await connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS trips 
                (
                    id SERIAL PRIMARY KEY,
                    train_number VARCHAR(4) NOT NULL,
                    departure_station_code INT NOT NULL CHECK 
                    (departure_station_code >= 2200000 AND departure_station_code <= 2299999),
                    arrival_station_code INT NOT NULL CHECK 
                    (arrival_station_code >= 2200000 AND arrival_station_code <= 2299999),
                    departure_time TIMESTAMPTZ NOT NULL,
                    arrival_time TIMESTAMPTZ NOT NULL
                )
                '''
            )

    async def create(self, trip: Trip) -> Trip:
        async with self.db.get_connection() as connection:
            try:
                row = await connection.fetchrow(
                    '''
                    INSERT INTO trips 
                    (train_number, departure_station_code, arrival_station_code, departure_time, arrival_time)
                    VALUES ($1, $2, $3, $4, $5)
                    RETURNING 
                    train_number, departure_station_code, arrival_station_code, departure_time, arrival_time
                    ''',
                    trip.train_number,
                    trip.departure_station_code,
                    trip.arrival_station_code,
                    trip.departure_time,
                    trip.arrival_time
                )
                return Trip(**row) if row else None
            except asyncpg.exceptions.DataError:
                raise HTTPException(status_code=400, detail="Invalid data")

    async def list(
            self,
            departure_station_code: int,
            arrival_station_code: int,
            departure_time: datetime,
            arrival_time: datetime
    ) -> List[Trip]:
        try:
            async with self.db.get_connection() as connection:
                rows = await connection.fetch(
                    '''
                    SELECT
                    train_number, departure_station_code, arrival_station_code, departure_time, arrival_time
                    FROM trips
                    WHERE departure_station_code = $1 AND arrival_station_code = $2
                    AND departure_time >= $3 AND arrival_time <= $4
                    ''',
                    departure_station_code,
                    arrival_station_code,
                    departure_time,
                    arrival_time
                )
                return [Trip(**row) for row in rows] if rows else []
        except asyncpg.exceptions.DataError:
            raise HTTPException(status_code=400, detail="Invalid data")

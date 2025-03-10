from datetime import datetime
from typing import List
from pydantic import BaseModel, constr, conint, field_validator, model_validator, Field


class Station(BaseModel):
    """
    Class representing a station model.

    Attributes:
    name: str - station name (min length 3, max length 64, only letters, numbers, hyphens and apostrophes)
    code: int - station code (between 2200000 and 2299999)
    """
    name: constr(
        min_length=3, max_length=64, pattern=r"^[А-Яа-яІЇЄҐієїґ0-9'-]{3,}$"
    ) = Field(..., example='Київ-Пасажирський-5')
    code: conint(ge=2200000, le=2299999)


class Wagon(BaseModel):
    """
    Class representing a wagon model.

    Attributes:
    number: str - wagon number (3 digits followed by 'К', 'Л' or 'П')
    """
    number: constr(min_length=3, max_length=3, pattern=r"^\d{2}[КЛП]$")


class Train(BaseModel):
    """
    Class representing a train model.

    Attributes:
    number: str - train number (4 digits followed by a letter)
    wagons: List[Wagon] - list of wagons (at least 1 wagon, all wagon numbers must be unique)
    """
    number: constr(
        min_length=4, max_length=4, pattern=r"^\d{3}[А-ЯІЇЄҐ]$"
    ) = Field(..., example='123А')
    wagons: List[Wagon] = Field(..., example=[{"number": "01К"}, {"number": "02Л"}])

    @field_validator('wagons')
    @classmethod
    def validate_wagons(cls, value: List[Wagon]) -> List[Wagon]:
        if len(value) < 1:
            raise ValueError('Wagons list must contain at least 1 wagon')

        wagon_numbers = [wagon.number for wagon in value]
        if len(wagon_numbers) != len(set(wagon_numbers)):
            raise ValueError('All wagon numbers must be unique')
        return value


class Trip(BaseModel):
    """
    Class representing a trip model.

    Attributes:
    train_number: str - train number (4 digits followed by a letter)
    departure_station_code: int - departure station code (between 2200000 and 2299999)
    arrival_station_code: int - arrival station code (between 2200000 and 2299999)
    departure_time: datetime - departure time
    arrival_time: datetime - arrival time
    """
    train_number: constr(
        min_length=4, max_length=4, pattern="^\d{3}[А-ЯІЇЄҐ]$"
    ) = Field(..., example='123А')
    departure_station_code: conint(ge=2200000, le=2299999)
    arrival_station_code: conint(ge=2200000, le=2299999)
    departure_time: datetime
    arrival_time: datetime

    @model_validator(mode='after')
    def validate_stations(self) -> 'Trip':
        if self.arrival_station_code == self.departure_station_code:
            raise ValueError('Arrival station code must be different from departure station code')
        return self

    @model_validator(mode='after')
    def validate_times(self) -> 'Trip':
        if self.arrival_time <= self.departure_time:
            raise ValueError('Arrival time must be later than departure time')
        return self

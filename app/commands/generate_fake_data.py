import asyncio

from faker import Faker
from app.dependencies import stations_repo, trains_repo, trips_repo, db
from app.models import Station, Train, Wagon, Trip

fake = Faker('uk_UA')


async def generate_fake_data():
    await db.connect()

    for _ in range(100):
        station = Station(
            name=fake.city().translate(str.maketrans('', '', '.()')).replace(' ', '-'),
            code=_ + 2200000
        )
        try:
            await stations_repo.create(station)
        except Exception as e:
            print(e)

    trains = []
    for _ in range(100):
        train_number = f"{str(_).zfill(3)}{fake.random_element(list('АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'))}"
        wagons = ["01К", "02Л", "03П", "04К", "05Л", "06П", "07К", "08Л", "09П", "10К"]
        train = Train(
            number=train_number,
            wagons=[Wagon(number=wagon) for wagon in wagons]
        )
        trains.append(train)
        await trains_repo.create(train.number, [wagon for wagon in wagons])

    stations = await stations_repo.list()

    for _ in range(999):
        departure = fake.date_time_this_month()
        arrival = fake.date_time_between(start_date=departure, end_date='+3d')
        departure_code = fake.random_element(stations).code
        arrival_code = fake.random_element(stations).code

        if departure_code == arrival_code:
            arrival_code += 1

        trip = Trip(
            train_number=fake.random_element(trains).number,
            departure_station_code=departure_code,
            arrival_station_code=arrival_code,
            departure_time=departure,
            arrival_time=arrival
        )
        await trips_repo.create(trip)

    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(generate_fake_data())

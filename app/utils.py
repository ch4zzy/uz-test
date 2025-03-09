async def normalize_wagons(train):
    """
    Normalize wagon numbers by sorting and renumbering them.

    Attributes:
    :param train:
    :return renumbered_wagons:
    """
    wagon_numbers = [wagon.number for wagon in train.wagons]
    sorted_wagons = sorted(wagon_numbers, key=lambda x: x[:2])
    renumbered_wagons = [f"{str(i + 1).zfill(2)}{wagon[2]}" for i, wagon in enumerate(sorted_wagons)]
    return renumbered_wagons

import asyncio
from dataclasses import dataclass
from enum import IntEnum
import random
import os


class CarBrokenError(Exception):
    pass


class IncorrectAddressError(Exception):
    pass


class PackingType(IntEnum):
    ENVELOPE = 0
    BOX = 1
    TUBE = 2
    ROLL = 3


@dataclass
class Package:
    # Unique identifier of a package
    idx: int
    # Lenght, width, height in cm
    dimensions: tuple[int, int, int]
    # Weight in kg
    weight: float
    type: PackingType


class PickupBox:
    """
    Represents a box of packages to deliver
    """
    max_packages = 64

    def __init__(self, packages: list[Package]):
        if len(packages) > self.max_packages:
            raise ValueError(f"Too many packages for pick up: {len(packages)}")

        self.__packages = packages

    def __len__(self) -> int:
        return len(self.__packages)

    @property
    def packages(self) -> list[Package]:
        return self.__packages


class DeliveryGenerator:
    """
    Generates new packages for delivery
    """

    def __iter__(self) -> "DeliveryGenerator":
        return self

    def __next__(self):
        return next(self.__generate())

    @staticmethod
    def __generate() -> Package:
        idx = 0
        while True:
            type = random.choice(list(PackingType))
            dimensions = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 10))
            weight = random.random() * 100
            package = Package(idx=idx, dimensions=dimensions, weight=weight, type=type)
            idx += 1

            yield package


class PickUpCar:
    """
    A car can only pickup a box of packages and the driver will deliver them one by one
    """
    async def deliver_box(self, pickup_box: PickupBox):
        """
        Deliver box of packages
        :param pickup_box: box of packages to deliver
        :return: <TODO>
        """
        # TODO: Implement box delivery
        pass

    async def __deliver_package(self, package: Package) -> Package:
        """
        Deliver one package
        :param package: package to deliver
        :return: package if the delivery was successful
        :raises:
            - CarBrokenError
            - IncorrectAddressError
        """
        rnd: float = random.random()
        match rnd:
            case rnd if rnd > 0.99:
                raise CarBrokenError()
            case rnd if 0.98 < rnd <= 0.99:
                raise IncorrectAddressError()
            case _:
                await asyncio.sleep(0.01)
                return package


if __name__ == '__main__':
    delivery_generator = DeliveryGenerator()
    cars = [PickUpCar() for _ in range(os.cpu_count())]

    # TODO: Create queues, iterate over packages, deliver boxes, etc.
    # Good luck!

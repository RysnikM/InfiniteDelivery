import random

from Services.data.repo.abs_repo import AbsRepo
from Services.domain.entity.enum import PackingType
from Services.domain.entity.pachage import Package


class DeliveryGenerator(AbsRepo):
    """
    Generates new packages for delivery
    """
    def __init__(self):
        self.g = self.__generate()

    def __iter__(self) -> "DeliveryGenerator":
        return self

    def __next__(self):
        return next(self.g)

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

    def get(self) -> Package:
        return next(self)

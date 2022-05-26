from dataclasses import dataclass

from Services.domain.entity.enum import PackingType


@dataclass
class Package:
    # Unique identifier of a package
    idx: int
    # Lenght, width, height in cm
    dimensions: tuple[int, int, int]
    # Weight in kg
    weight: float
    type: PackingType
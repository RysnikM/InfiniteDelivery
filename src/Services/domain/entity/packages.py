from pydantic import Field
from pydantic.dataclasses import dataclass

from Services.domain._utils import MyDataclass
from Services.domain.entity.enums import PackingType

length = int
width = int
height = int
kg = float


@dataclass
class PackageEnt(MyDataclass):
    idx: int

    dimensions: tuple[length, width, height]
    weight: kg

    type: PackingType


@dataclass
class BoxEnt(MyDataclass):
    max_packages = 64

    packages: list[PackageEnt] = Field(default_factory=lambda: [])

    @property
    def is_filled(self) -> bool:
        return True if len(self.packages) >= self.max_packages else False

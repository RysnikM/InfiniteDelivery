from enum import Enum


class PackingType(int, Enum):
    ENVELOPE = 0
    BOX = 1
    TUBE = 2
    ROLL = 3

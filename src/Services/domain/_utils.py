from enum import Enum
from dataclasses import asdict

from pydantic.dataclasses import dataclass


@dataclass
class MyDataclass:
    def as_dict(self):
        return asdict(self, dict_factory=asdict_factory)


def asdict_factory(data):
    def convert_value(obj):
        if isinstance(obj, Enum):
            return obj.value
        return obj

    return dict((k, convert_value(v)) for k, v in data)

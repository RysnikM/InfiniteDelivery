from abc import ABC, abstractmethod


class AbsRepo(ABC):
    @abstractmethod
    def get(self): ...

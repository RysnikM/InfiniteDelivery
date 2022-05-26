from unittest import TestCase

from Services.data.repo.storage_repo import PackageStorageRepo
from Services.domain.entity.packages import PackageEnt


class TestDeliveryGenerator(TestCase):
    gen = PackageStorageRepo()

    """ Success """

    def test01(self):
        assert next(self.gen) != next(self.gen)

    def test_idx(self):
        assert next(self.gen).idx != next(self.gen).idx

    def test_get(self):
        assert self.gen.get()
        assert isinstance(self.gen.get(), PackageEnt)

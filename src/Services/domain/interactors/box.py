import logging

from Services.config import QUEUE_PACKAGES_NAME
from Services.data.repo.storage_repo import PackageStorageRepo
from Services.domain.entity.packages import BoxEnt
from Services.data.services.queue_interface import QueueInterface

logger = logging.getLogger(__name__)


class BoxInteractor:
    def __call__(self, package_storage: PackageStorageRepo, packages_queue: QueueInterface):
        self.package_storage = package_storage

        self.packages_queue = packages_queue
        self.packages_queue(QUEUE_PACKAGES_NAME)

        self.box = BoxEnt()

    def prepare_box_to_delivery(self) -> BoxEnt:
        logger.info(f"Prepare box")
        while True:
            self.box.packages.append(self.package_storage.get())
            if self.box.is_filled:
                logger.info(f"Success filled box")
                return self.box

    def push_to_packages_queue(self, box: BoxEnt) -> None:
        logger.debug(f"Try push new box to delivery queue")
        self.packages_queue.push_stream(message=box.as_dict())

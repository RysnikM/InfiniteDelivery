import random
import asyncio
import logging

from Services.config import QUEUE_DELIVERED_NAME, QUEUE_NO_DELIVERED_NAME, QUEUE_DEAD_LETTER_PACKAGES_NAME
from Services.common.custom_errors import CarBrokenError, IncorrectAddressError
from Services.domain.entity.packages import BoxEnt, PackageEnt
from Services.data.services.queue_interface import QueueInterface

logger = logging.getLogger(__name__)


class PickUpCarInteractor:
    def __call__(
        self,
        dead_letter_packages_queue: QueueInterface,
        delivered_queue: QueueInterface,
        no_delivered_queue: QueueInterface,
    ):
        self.dead_letter_packages_queue = dead_letter_packages_queue
        self.delivery_queue = delivered_queue
        self.no_delivery_queue = no_delivered_queue

        self.dead_letter_packages_queue(QUEUE_DEAD_LETTER_PACKAGES_NAME)
        self.delivery_queue(QUEUE_DELIVERED_NAME)
        self.no_delivery_queue(QUEUE_NO_DELIVERED_NAME)

    def push_to_dead_letter_packages_queue(self, package: PackageEnt) -> None:
        logger.info(f"Try push new box to packages queue")
        # self.delivery_queue.push(queue_name=QUEUE_DEAD_LETTER_PACKAGES_NAME, message=package.as_dict())
        self.dead_letter_packages_queue.push_stream(message=package.as_dict())

    def push_to_delivered_queue(self, package: PackageEnt) -> None:
        logger.info(f"Try push new box to deliverer queue")
        # self.delivery_queue.push(queue_name=QUEUE_DELIVERED_NAME, message=package.as_dict())
        self.delivery_queue.push_stream(message=package.as_dict())

    def push_to_no_delivered_queue(self, package: PackageEnt) -> None:
        logger.info(f"Try push new box to no delivered queue")
        # self.delivery_queue.push(queue_name=QUEUE_NO_DELIVERED_NAME, message=package.as_dict())
        self.no_delivery_queue.push_stream(message=package.as_dict())

    async def deliver_box(self, box: BoxEnt):
        """
        Deliver box of packages
        :param box: box of packages to deliver
        """
        for package in box.packages:
            try:
                result = await self.__deliver_package(package)
                logger.info(f"Success delivered package {result}")
                self.push_to_delivered_queue(package)
            except CarBrokenError:
                logger.warning(f"Car broken, package {package} return to queue")
                self.push_to_dead_letter_packages_queue(package)
            except IncorrectAddressError:
                logger.error(f"Address incorrect, delivered package {package} stopped")
                self.push_to_no_delivered_queue(package)

    @staticmethod
    async def __deliver_package(package: PackageEnt) -> PackageEnt:
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
                logger.info("success delivered package")
                return package

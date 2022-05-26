import random
import logging
from time import sleep

import ujson

from Services.config import (
    QUEUE_BROKER_URL,
    QUEUE_PACKAGES_NAME,
    QUEUE_DELIVERED_NAME,
    QUEUE_NO_DELIVERED_NAME,
    QUEUE_DEAD_LETTER_PACKAGES_NAME,
)
from Services.data.services.amqp import AmqpQueue
from Services.common.custom_errors import CarBrokenError, IncorrectAddressError
from Services.domain.entity.packages import BoxEnt, PackageEnt
from Services.data.services.queue_interface import QueueInterface

logger = logging.getLogger(__name__)


class PickUpCarInteractor:
    def __call__(
        self,
        packages_queue: QueueInterface,
        delivered_queue: QueueInterface,
        no_delivered_queue: QueueInterface,
    ):
        self.packages_queue = packages_queue
        self.delivery_queue = delivered_queue
        self.delivery_queue = no_delivered_queue

    def push_to_dead_letter_packages_queue(self, package: PackageEnt) -> None:
        logger.info(f"Try push new box to packages queue")
        self.delivery_queue.push(queue_name=QUEUE_DEAD_LETTER_PACKAGES_NAME, message=package.as_dict())

    def push_to_delivered_queue(self, package: PackageEnt) -> None:
        logger.info(f"Try push new box to deliverer queue")
        self.delivery_queue.push(queue_name=QUEUE_DELIVERED_NAME, message=package.as_dict())

    def push_to_no_delivered_queue(self, package: PackageEnt) -> None:
        logger.info(f"Try push new box to no delivered queue")
        self.delivery_queue.push(queue_name=QUEUE_NO_DELIVERED_NAME, message=package.as_dict())

    def deliver_box(self, box: BoxEnt):
        """
        Deliver box of packages
        :param box: box of packages to deliver
        """
        for package in box.packages:
            try:
                result = self.__deliver_package(package)
                logger.info(f"Success delivered package {result}")
                self.push_to_delivered_queue(package)
            except CarBrokenError:
                logger.warning(f"Car broken, package {package} return to queue")
                self.push_to_dead_letter_packages_queue(package)
            except IncorrectAddressError:
                logger.error(f"Address incorrect, delivered package {package} stopped")
                self.push_to_no_delivered_queue(package)

    @staticmethod
    def __deliver_package(package: PackageEnt) -> PackageEnt:
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
                sleep(0.01)
                logger.info("success delivered package")
                return package

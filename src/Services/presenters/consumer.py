import asyncio
import logging

import ujson
from aio_pika.abc import AbstractIncomingMessage

from Services.config import QUEUE_BROKER_URL, QUEUE_PACKAGES_NAME
from Services.data.services.amqp import AmqpQueue
from Services.domain.entity.packages import BoxEnt
from Services.domain.interactors.picup import PickUpCarInteractor

logger = logging.getLogger(__name__)

pickup_interactor = PickUpCarInteractor()
pickup_interactor(
    dead_letter_packages_queue=AmqpQueue(QUEUE_BROKER_URL),
    delivered_queue=AmqpQueue(QUEUE_BROKER_URL),
    no_delivered_queue=AmqpQueue(QUEUE_BROKER_URL),
)


async def async_callback_func(message: AbstractIncomingMessage):
    try:
        await pickup_interactor.deliver_box(BoxEnt(**ujson.loads(message.body)))
    except TypeError:
        logger.error(f"Validation error")


def consumer(channel_number: int):
    client = AmqpQueue(QUEUE_BROKER_URL)
    asyncio.run(client.async_consumer(QUEUE_PACKAGES_NAME, async_callback_func, channel_number=channel_number))

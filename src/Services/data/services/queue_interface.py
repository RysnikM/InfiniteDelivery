from typing import Callable

from pika import spec
from aio_pika.abc import AbstractIncomingMessage
from pika.adapters.blocking_connection import BlockingChannel


def on_message(channel, method, _, body):
    pass


async def asynch_on_message(message: AbstractIncomingMessage):
    pass


# typing alias
callback_func: Callable[[BlockingChannel, spec.Basic.Deliver, spec.BasicProperties, bytes], None] = on_message
async_callback_func: AbstractIncomingMessage = asynch_on_message


class QueueInterface:
    """
    Interface for Queue clients
    """

    def push(self, queue_name: str, message: dict, **kwargs) -> None:
        raise NotImplementedError

    def push_stream(self, message: dict) -> None:
        raise NotImplementedError

    def consumer(self, queue_name: str, callback: callback_func) -> None:
        raise NotImplementedError

    async def async_consumer(self, queue_name: str, callback: async_callback_func, channel_number: int = 1) -> None:
        raise NotImplementedError

from typing import Callable

from pika import spec
from pika.adapters.blocking_connection import BlockingChannel


def on_message(channel, method, _, body):
    pass


# typing alias
callback_func: Callable[[BlockingChannel, spec.Basic.Deliver, spec.BasicProperties, bytes], None] = on_message


class QueueInterface:
    """
    Interface for Queue clients
    """

    def push(self, queue_name: str, message: dict, **kwargs) -> None:
        ...

    def push_stream(self, message: dict) -> None:
        ...

    def consumer(self, queue_name: str, callback_func: callback_func) -> None:
        ...

import asyncio
import logging

import pika
import ujson as ujson
import aio_pika
from pika.adapters.blocking_connection import BlockingConnection

from Services.data.services.queue_interface import QueueInterface, callback_func, async_callback_func

logger = logging.getLogger(__name__)


class AmqpQueue(QueueInterface):
    """
    Amqp client
    """

    def __init__(self, url: str):
        """
        constructor
        Args:
            url: broker url path.
                Examples: queue://user:path@host:port/
        """
        self.url = url

    def __call__(self, queue_name: str, channel_number: int = 1) -> None:
        self.queue_name = queue_name
        self.conn = self._connect()
        self.channel = self.conn.channel(channel_number=channel_number)
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def _connect(self) -> BlockingConnection:
        connection = pika.BlockingConnection(pika.URLParameters(self.url))
        return connection

    def push(self, queue_name: str, message: dict, **kwargs) -> None:
        """
        Func for send a messages to queue
        Args:
            queue_name: queue name for push a messages
            message: message for sent to queue
        """
        conn = self._connect()
        with conn.channel() as channel:
            channel.queue_declare(queue=queue_name, durable=True)
            logger.info(f"try send message to queue")
            channel.basic_publish(exchange="", routing_key=queue_name, body=ujson.dumps(message).encode("utf-8"))
            logger.info(f"success send {message}")

    def push_stream(self, message: dict) -> None:
        """
        Func for send a messages to queue
        Args:
            queue_name: queue name for push a messages
            message: message for sent to queue
        """
        logger.info(f"try send message to queue")
        self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=ujson.dumps(message).encode("utf-8"))
        logger.info(f"success send {message}")

    def pop(self, queue_name: str) -> str | None:
        conn = self._connect()
        with conn.channel() as channel:
            channel.queue_declare(queue=queue_name, durable=True)
            method_frame, header_frame, body = channel.basic_get(queue=queue_name)
            if not body or method_frame.NAME == "Basic.GetEmpty":
                return None
            else:
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                return body

    def consumer(self, queue_name: str, callback: callback_func):
        """
        Args:
            queue_name: queue name
            callback: on_message callback func.
                Examples:
                     def on_message(channel, method, _, body): ...
            queue_name: queue name that the consumer is listening to

        """
        conn = self._connect()
        logger.info(f"Try run a consumer")
        with conn.channel() as channel:
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_qos(prefetch_count=10)
            channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
            logger.info(f"[x] consumer is run")
            channel.start_consuming()

    async def async_consumer(self, queue_name: str, callback: async_callback_func, channel_number: int = 1) -> None:
        """
        Args:
            channel_number: number of channel to connect
            queue_name: queue name
            callback: on_message callback func.
                Examples:
                     def on_message(channel, method, _, body): ...
            queue_name: queue name that the consumer is listening to

        """

        connection = await aio_pika.connect_robust(self.url, reconnect_interval=10.0)
        channel = await connection.channel(channel_number)
        # `prefetch_count` - maximum message count which will be processed at the same time.
        # For a true message balancing, set prefetch_count=1
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.consume(callback, no_ack=True)

        try:
            await asyncio.Future()
        finally:
            await connection.close()

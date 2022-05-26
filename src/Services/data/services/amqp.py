import time
import logging

import pika
import ujson as ujson
from pika.adapters.blocking_connection import BlockingConnection

from Services.config import QUEUE_BROKER_URL, QUEUE_PACKAGES_NAME
from Services.data.services.queue_interface import QueueInterface, callback_func

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
        self.received_message = None

    def __call__(self, queue_name: str) -> None:
        self.queue_name = queue_name
        self.conn = self._connect()
        self.channel = self.conn.channel()
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

    def consumer(self, queue_name: str, callback_func: callback_func):
        """
        Args:
            callback_func: on_message callback func.
                Examples:
                     def on_message(channel, method, _, body): ...
            queue_name: queue name that the consumer is listening to

        """
        conn = self._connect()
        logger.info(f"Try run a consumer")
        with conn.channel() as channel:
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback_func)
            logger.info(f"[x] consumer is run")
            channel.start_consuming()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    q = AmqpQueue(QUEUE_BROKER_URL)
    # q.consumer(QUEUE_PACKAGES_NAME)

    st = time.time()
    for _ in range(500):
        q.push(QUEUE_PACKAGES_NAME, {"message": time.time()})
    print(time.time() - st)

    # q(QUEUE_PACKAGES_NAME)
    # st = time.time()
    # for _ in range(500):
    #     q.push_stream(message={"m": time.time()})
    # print(time.time()-st)

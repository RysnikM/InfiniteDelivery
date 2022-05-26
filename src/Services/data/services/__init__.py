from Services.config import QUEUE_BROKER_URL
from Services.data.services.amqp import AmqpQueue

queue_services = AmqpQueue(QUEUE_BROKER_URL)

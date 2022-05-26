import ujson

from Services.config import QUEUE_BROKER_URL, QUEUE_PACKAGES_NAME
from Services.data.services import queue_services
from Services.data.services.amqp import AmqpQueue
from Services.domain.entity.packages import BoxEnt
from Services.domain.interactors.picup import PickUpCarInteractor

pickup_interactor = PickUpCarInteractor()
pickup_interactor(
    packages_queue=AmqpQueue(QUEUE_BROKER_URL),
    delivered_queue=AmqpQueue(QUEUE_BROKER_URL),
    no_delivered_queue=AmqpQueue(QUEUE_BROKER_URL),
)


def callback_func(*args):
    channel, method, _, body = args
    pickup_interactor.deliver_box(BoxEnt(**ujson.loads(body)))


def consumer():
    queue_services.consumer(QUEUE_PACKAGES_NAME, callback_func=callback_func)

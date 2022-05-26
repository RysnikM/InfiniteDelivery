import logging
import concurrent.futures
from multiprocessing import cpu_count

from Services.data.services import queue_services
from Services.presenters.consumer import consumer
from Services.data.repo.storage_repo import PackageStorageRepo
from Services.domain.interactors.box import BoxInteractor

logger = logging.getLogger(__name__)


box_interactor = BoxInteractor()


def publish_box():
    """Box creator process"""
    # init box interactor
    box_interactor(package_storage=PackageStorageRepo(), packages_queue=queue_services)
    while True:
        # create box & push box in to delivery queue
        box_interactor.push_to_packages_queue(box=box_interactor.prepare_box_to_delivery())


def main():
    NUM_CORES = cpu_count()
    process = []

    max_workers = NUM_CORES
    # create process pool
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        process.append(executor.submit(consumer, channel_number=2))
        process.append(executor.submit(publish_box))

    concurrent.futures.wait(process)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()

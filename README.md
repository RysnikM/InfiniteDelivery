# InfiniteDelivery

---
link to RabbitMQ panel:  http://0.0.0.0:15671/ 

base credentials: guest/guest;

---
For run needs:
1. Install docker, docker-compose;
2. Install make tools;
```bash
# linux:
sudo apt install make

# mackos:
brew install make 
```
3. Build containers;
```bach
make build
```
3. Create `.env` file in project root directory with variables:
```text
SERVER_TYPE=local
QUEUE_BROKER_URL=amqp://guest:guest@rabbit:5672/
QUEUE_PACKAGES_NAME=packages_queue
QUEUE_DEAD_LETTER_PACKAGES_NAME=dead_letter_packages_queue
QUEUE_DELIVERED_NAME=delivered_queue
QUEUE_NO_DELIVERED_NAME=no_delivered_queue
```
4. Run containers:
```bash
make local
```
5. If needed to see logs from application container:
```bash
docker logs -f app
```
6. For stop / down containers:
```bash
make stop # fro stop containers
make down # for down containers
```

> Before start compose make sure the ports 5672 and 15671 are available
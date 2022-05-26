SERVICES_NAME=delivery_system

#######################################################################################################################
refactor:
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				src/
	black src/
	isort src/
	echo "-----CHECK STATUS-----"
	make lint
lint:
	autoflake --in-place --recursive src/ --check
	black src/ --check
	isort src/ --check-only --skip src/DAG/
	mypy src/

# RUN SECTION
local:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml up -d
dev:
	TAG=dev docker-compose -f docker-compose-base.yml up -d

down:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml down

# COMMON SECTION
prune:
	docker system prune -f

# BUILD PART
build:
	docker build -t ${SERVICES_NAME}/app -f Dockerfile .
	make prune

build-dev:
	docker build -t ${SERVICES_NAME}/app:dev -f Dockerfile .
	make prune

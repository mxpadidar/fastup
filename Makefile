PACKAGE ?= fastup
MAKEFLAGS += --no-print-directory

DATA_DIR = ${PWD}/.cache

PG_NAME = fastup_dev
PG_USER = fastup
PG_PASSWORD = secret
PG_PORT = 5432
PG_IMAGE = docker.io/library/postgres:18.0-trixie
PG_CONTAINER = fastup-postgres

REDIS_CONTAINER = fastup-redis
REDIS_IMAGE = docker.io/library/redis:8.4.0-alpine
REDIS_PORT = 6379


.PHONY: all run install fmt lint type-check test
all: install fmt lint type-check test
	@echo "-> ready to go!"

run:
	@uv run python -m $(PACKAGE).main

install:
	@echo "-> syncing dependencies"
	@uv sync

fmt:
	@echo "-> formatting code (ruff)"
	@uv run ruff format

lint:
	@echo "-> linting (ruff)"
	@uv run ruff check --fix

type-check:
	@echo "-> type checking (pyright)"
	@uv run pyright fastup

test:
		@echo "-> running tests with coverage"
		@uv run pytest --cov=$(PACKAGE) --cov-report=html --cov-report=term-missing

.PHONY: pgup pgdown pgshell pgclean pglogs
pgup:
	@mkdir -p $(DATA_DIR)/pgdata
	@podman run --replace -d \
		--name $(PG_CONTAINER) \
		-e POSTGRES_USER=$(PG_USER) \
		-e POSTGRES_PASSWORD=$(PG_PASSWORD) \
		-e POSTGRES_DB=$(PG_NAME) \
		-p $(PG_PORT):5432 \
		-v $(DATA_DIR)/pgdata:/var/lib/postgresql \
		$(PG_IMAGE) >/dev/null
	@echo "-> postgresql is ready"

pgclean: pgdown
	@echo "-> cleaning up postgresql container and volume"
	@podman rm -f $(PG_CONTAINER) >/dev/null 2>&1 || true
	@sudo rm -rf $(DATA_DIR)/pgdata

pgdown:
	@echo "-> stopping postgresql container"
	@podman stop $(PG_CONTAINER) >/dev/null 2>&1 || true

pgshell:
	@podman exec -it $(PG_CONTAINER) psql -U $(PG_USER) -d $(PG_NAME)

.PHONY: migrations migrate rollback-migration
migrations:
		@read -p "enter migration message: " message; \
		uv run alembic revision --autogenerate -m "$$message"

migrate:
		@uv run alembic upgrade head

rollback-migration:
		@uv run alembic downgrade -1
		@echo "-> consider manually removing the migration file if necessary."

.PHONY: redisup redisdown rediscli redisclean
redisup:
	@mkdir -p $(DATA_DIR)/redis
	@podman run --replace -d \
		--name $(REDIS_CONTAINER) \
		-p $(REDIS_PORT):6379 \
		-v $(DATA_DIR)/redis:/data \
		$(REDIS_IMAGE) redis-server --appendonly yes >/dev/null
	@echo "-> Redis is ready"

redisdown:
	@echo "-> stopping Redis container"
	@podman stop $(REDIS_CONTAINER) >/dev/null 2>&1 || true

redisclean: redisdown
	@echo "-> cleaning up Redis container and data volume"
	@podman rm -f $(REDIS_CONTAINER) >/dev/null 2>&1 || true
	@sudo rm -rf $(REDIS_DATA)

rediscli:
	@podman exec -it $(REDIS_CONTAINER) redis-cli

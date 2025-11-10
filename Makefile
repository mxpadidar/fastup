PACKAGE ?= fastup
LOG_CONFIG ?= ./logging.yaml
PORT ?= 8000

REDIS_IMAGE ?= docker.io/library/redis:8.4-rc1
REDIST_VAOLUME_DIR ?= $(PWD)/.cache/redis-data
REDIS_PORT ?= 6379
REDIS_CONTAINER ?= $(PACKAGE)-redis


.PHONY: run install fmt lint type-check test all

run:
	@uv run uvicorn ${PACKAGE}.entrypoints.app:app --host 0.0.0.0 \
		--port ${PORT} --reload --log-config=${LOG_CONFIG}

worker:
	@uv run celery -A ${PACKAGE}.entrypoints.worker worker

dev:
	@uv run honcho start

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
	@echo "-> type checking (ty)"
	@uv run ty check

test:
	@echo "-> running tests with coverage"
	@uv run pytest --cov=$(PACKAGE) --cov-report=html --cov-report=term-missing


all: install fmt lint type-check test
	@echo "-> ready to go!"

.PHONY: migrations migrate rollback-migration
migrations:
	@read -p "enter migration message: " message; \
	uv run alembic revision --autogenerate -m "$$message"

migrate:
	@uv run alembic upgrade head

rollback-migration:
	@uv run alembic downgrade -1
	@echo "consider manually removing the migration file if necessary."

# podman redis helpers
.PHONY: redis-up redis-down redis-shell
redis-up:
	@mkdir -p "$(REDIST_VAOLUME_DIR)"
	@podman run -d --name $(REDIS_CONTAINER) -p $(REDIS_PORT):$(REDIS_PORT) -v "$(REDIST_VAOLUME_DIR):/data:Z" $(REDIS_IMAGE)

redis-down:
	@podman rm -f $(REDIS_CONTAINER)

redis-shell:
	@podman exec -it $(REDIS_CONTAINER) redis-cli

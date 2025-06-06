# load .env file if it exists
ifneq (,$(wildcard .env))
	include .env
	export
endif

PGDATA_DIR=.cache/pgdata
POSTGRES_CONTAINER=dev-postgres
POSTGRES_IMAGE=docker.io/postgres:17-bookworm

load-env:
	@echo "Loading environment variables from .env file..."
	@if [ -f .env ]; then \
		export $(cat .env | sed 's/#.*//g' | xargs); \
	else \
		echo ".env file not found."; \
	fi

.PHONY: start-db psql stop-db clean-db
start-db:
	@mkdir -p $(PGDATA_DIR)
	@podman run -d --rm \
		--name $(POSTGRES_CONTAINER) \
		-p $(POSTGRES_PORT):5432 \
		-e POSTGRES_USER=$(POSTGRES_USER) \
		-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		-e POSTGRES_DB=$(POSTGRES_DB) \
		-e POSTGRES_HOST=$(POSTGRES_HOST) \
		-v $(PWD)/$(PGDATA_DIR):/var/lib/postgresql/data:Z $(POSTGRES_IMAGE)
	@echo "PostgreSQL container is running."

psql:
	@podman exec -e PGPASSWORD=$(POSTGRES_PASSWORD) -it $(POSTGRES_CONTAINER) \
		psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

stop-db:
	@podman stop $(POSTGRES_CONTAINER) || true

clean-db: stop-db
	@rm -rf $(PGDATA_DIR)

.PHONY: start-server test check install lint typecheck tree
start-server:
	@echo "Starting server on $(SERVER_HOST):$(SERVER_PORT)..."
	uv run uvicorn fastup.main:app --host $(SERVER_HOST) --port $(SERVER_PORT) --reload

test:
	uv run pytest tests/

check: lint typecheck

install:
	uv sync

lint:
	uvx ruff check fastup/ tests/ --fix

typecheck:
	uvx pyright fastup/ tests/

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv|.local"

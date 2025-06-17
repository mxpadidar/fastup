# Load environment variables from .env file.
# having a .env file is required for this makefile to work.
include .env

DB_DATA=.cache/db_data
DB_CONTAINER=dev-db
DB_IMAGE=docker.io/postgres:17-bookworm

.PHONY: install runserver all test lint typecheck init-pgdata run-db stop-db psql clean tree
install:
	uv sync

run-server:
	uv run uvicorn fastup.app:app --host $(SERVER_HOST) --port $(SERVER_PORT) --reload

all: lint typecheck test

test:
	uv run pytest tests/

lint:
	uv run ruff check fastup/ tests/ --fix

typecheck:
	uv run pyright fastup/ tests/

init-pgdata:
	@mkdir -p $(DB_DATA)

run-db: init-pgdata
	@podman run -d --name $(DB_CONTAINER) \
		-p $(DB_PORT):5432 \
		-v $(PWD)/$(DB_DATA):/var/lib/postgresql/data:Z \
		-e POSTGRES_USER=$(DB_USER) \
		-e POSTGRES_PASSWORD=$(DB_PASSWORD) \
		-e POSTGRES_DB=$(DB_DB) \
		$(DB_IMAGE)

stop-db:
	@podman stop $(DB_CONTAINER) || true

remove-db:
	@podman rm $(DB_CONTAINER) || true

psql:
	@podman exec -e PGPASSWORD=$(DB_PASSWORD) -it $(DB_CONTAINER) \
		psql -U $(DB_USER) -d $(DB_DB)

clean: stop-db remove-db
	@for name in __pycache__ .cache .venv; do \
		if ! rm -rf "$$name" 2>/dev/null; then \
			sudo rm -rf "$$name" 2>/dev/null; \
		fi \
	done

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv"


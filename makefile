# having a .env file is required for this makefile to work.
include .env

DB_DATA=.cache/db-data
DB_CONTAINER=db-dev
DB_IMAGE=docker.io/postgres:17-bookworm

.PHONY: runserver install test lint type-check 
runserver:
	@uv run python -m fastup.app

install:
	@uv sync

test:
	@uv run pytest tests/

lint:
	@uv run ruff check fastup/ tests/ --fix

type-check:
	@uv run pyright fastup/ tests/

.PHONY: db-up db-down db-clean psql
db-up:
	@mkdir -p $(DB_DATA) && \
		podman run -d --replace --name $(DB_CONTAINER) \
		-p $(DB_PORT):5432 \
		-v $(PWD)/$(DB_DATA):/var/lib/postgresql/data:Z \
		-e POSTGRES_USER=$(DB_USER) \
		-e POSTGRES_PASSWORD=$(DB_PASSWORD) \
		-e POSTGRES_DB=$(DB_NAME) \
		$(DB_IMAGE) > /dev/null && \
		echo "container $(DB_CONTAINER) is up and running on port $(DB_PORT)."

db-down:
	@podman stop $(DB_CONTAINER) > /dev/null 2>&1 || true \
		&& echo "container $(DB_CONTAINER) stopped."

db-clean: db-down
	@podman rm $(DB_CONTAINER) > /dev/null 2>&1 || true \
		&& echo "container $(DB_CONTAINER) removed."
	@sudo rm -rf $(DB_DATA) \
		&& echo "data directory $(DB_DATA) removed."

psql:
	@podman exec -e PGPASSWORD=$(DB_PASSWORD) -it $(DB_CONTAINER) \
		psql -U $(DB_USER) -d $(DB_NAME)

.PHONY: all clean tree
all: test lint type-check

clean: db-clean
	@for name in __pycache__ .cache .venv; do \
		echo "deleting $$name..."; \
		find . -name "$$name" -exec rm -rf {} + ;\
	done

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv"


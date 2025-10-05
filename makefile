POSTGRES_USER						:= fastup
POSTGRES_PASSWORD				:= pg-secret
POSTGRES_PORT						:= 5433
POSTGRES_DATABASE_NAME	:= fastup-dev
POSTGRES_HOST						:= localhost
POSTGRES_CONTAINER_NAME	:= ${POSTGRES_DATABASE_NAME}-container
POSTGRES_IMAGE 					:= docker.io/postgres:18.0-bookworm
POSTGRES_DATA_DIR				:= .cache/pgdata

.PHONY: run install test lint type-check all clean tree
run:
	@POSTGRES_USER=$(POSTGRES_USER) POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	POSTGRES_PORT=$(POSTGRES_PORT) POSTGRES_HOST=$(POSTGRES_HOST) \
	POSTGRES_DATABASE_NAME=$(POSTGRES_DATABASE_NAME) \
	uv run python -m fastup.main

test:
	@POSTGRES_USER=$(POSTGRES_USER) POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	POSTGRES_PORT=$(POSTGRES_PORT) POSTGRES_HOST=$(POSTGRES_HOST) \
	POSTGRES_DATABASE_NAME=$(POSTGRES_DATABASE_NAME) \
	uv run pytest tests --cov=fastup

install:
	@uv sync

lint:
	@uv run ruff check fastup/ tests/ --fix

type-check:
	@uv run pyright fastup/ tests/

all: install lint type-check test

clean:
	@for name in __pycache__ .cache .venv; do \
		echo "deleting $$name..."; \
		find . -name "$$name" -exec rm -rf {} + ;\
	done

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv"

.PHONY: pg-start pg-stop pg-clean psql
pg-start:
	@mkdir -p $(POSTGRES_DATA_DIR)
	@podman run -d --replace \
		--name $(POSTGRES_CONTAINER_NAME) \
		-e POSTGRES_USER=$(POSTGRES_USER) \
		-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		-e POSTGRES_DB=$(POSTGRES_DATABASE_NAME) \
		-v $(abspath $(POSTGRES_DATA_DIR)):/var/lib/postgresql/data \
		-p $(POSTGRES_PORT):5432 $(POSTGRES_IMAGE) \
	&& echo "postgres container $(POSTGRES_CONTAINER_NAME) started." \
	|| echo "failed to start postgres container."

psql:
	@podman exec -it $(POSTGRES_CONTAINER_NAME) psql -U $(POSTGRES_USER) -d $(POSTGRES_DATABASE_NAME)

pg-stop:
	@podman stop $(POSTGRES_CONTAINER_NAME) && echo "postgres container stopped."

pg-clean: pg-stop
	@podman rm $(POSTGRES_CONTAINER_NAME) 2>/dev/null || true
	@podman unshare rm -rf $(POSTGRES_DATA_DIR) 2>/dev/null || sudo rm -rf $(POSTGRES_DATA_DIR)
	@echo "postgres container and data cleaned."

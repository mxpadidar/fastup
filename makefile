POSTGRES_USER						:= fastup
POSTGRES_PASSWORD				:= pg-secret
POSTGRES_PORT						:= 5433
POSTGRES_DATABASE_NAME	:= fastup-dev
POSTGRES_HOST						:= localhost
POSTGRES_CONTAINER_NAME	:= ${POSTGRES_DATABASE_NAME}-container
POSTGRES_IMAGE 					:= docker.io/postgres:17.5-bookworm
POSTGRES_DATA_DIR				:= .cache/pgdata

.PHONY: run install test lint type-check all clean tree
run:
	@POSTGRES_USER=$(POSTGRES_USER) POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	POSTGRES_PORT=$(POSTGRES_PORT) POSTGRES_HOST=$(POSTGRES_HOST) \
	POSTGRES_DATABASE_NAME=$(POSTGRES_DATABASE_NAME) \
	uv run python -m fastup.main

install:
	@echo "installing dependencies..."
	@uv sync

push-main:
	@echo "pushing changes to main branch..."
	@git push origin -u main --force-with-lease

test:
	@echo "running tests..."
	@uv run pytest tests --cov=fastup

lint:
	@echo "running linter..."
	@uv run ruff check fastup/ tests/ --fix

type-check:
	@echo "running type checker..."
	@uv run pyright fastup/ tests/

all: install lint type-check test

clean:
	@for name in __pycache__ .cache .venv; do \
		echo "deleting $$name..."; \
		find . -name "$$name" -exec rm -rf {} + ;\
	done

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv"

.PHONY: pg-start psql pg-stop pg-clean
pg-start:
	@mkdir -p $(POSTGRES_DATA_DIR)
	@podman run -d --rm --replace \
	--name $(POSTGRES_CONTAINER_NAME) \
	-e POSTGRES_USER=$(POSTGRES_USER) \
	-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	-e POSTGRES_DB=$(POSTGRES_DATABASE_NAME) \
	-v $(abspath $(POSTGRES_DATA_DIR)):/var/lib/postgresql/data \
	-p $(POSTGRES_PORT):5432 $(POSTGRES_IMAGE) > /dev/null 2>&1 || true && \
	echo "postgres container $(POSTGRES_CONTAINER_NAME) started." || \
	echo "failed to start postgres container $(POSTGRES_CONTAINER_NAME)."

psql:
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql \
	-h $(POSTGRES_HOST) -p $(POSTGRES_PORT) \
	-U $(POSTGRES_USER) $(POSTGRES_DATBASE_NAME) 2> /dev/null || \
	(echo "failed to connect to postgresql, is the container running?" && true)

pg-stop:
	@podman stop $(POSTGRES_CONTAINER_NAME) > /dev/null 2>&1 || true \
	&& echo "container $(POSTGRES_CONTAINER_NAME) stopped." || \
	echo "failed to stop container $(POSTGRES_CONTAINER_NAME)."

pg-clean: pg-stop
	@podman rm $(POSTGRES_CONTAINER_NAME) > /dev/null 2>&1 || true \
	&& echo "container $(POSTGRES_CONTAINER_NAME) removed." || \
	echo "failed to remove container $(POSTGRES_CONTAINER_NAME)."
	@podman unshare rm -rf $(POSTGRES_DATA_DIR) \
	&& echo "data directory $(POSTGRES_DATA_DIR) removed." || \
	echo "failed to remove data directory $(POSTGRES_DATA_DIR)."

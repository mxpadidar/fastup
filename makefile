# Load environment variables from .env file.
# having a .env file is required for this makefile to work.
include .env

.PHONY: install runserver all test lint typecheck
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

.PHONY: clean tree
clean:
	@for name in __pycache__ .cache .venv; do \
		echo "Deleting $$name..."; \
		find . -name "$$name" -exec rm -rf {} + ;\
	done

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv"


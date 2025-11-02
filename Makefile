PACKAGE ?= fastup

.PHONY: run install fmt lint type-check test all

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

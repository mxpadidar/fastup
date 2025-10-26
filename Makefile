.PHONY: run install fmt type-check test coverage all
run:
	@uv run python -m app.main

install:
	@uv sync

fmt:
	@uv run ruff check . --fix
	@uv run ruff format .

type-check:
	@uv run pyright .

test:
	@uv run pytest --no-cov

coverage:
	@rm -rf htmlcov .coverage
	@uv run pytest --cov=app --cov-report=term-missing --cov-report=html

all: install fmt type-check test

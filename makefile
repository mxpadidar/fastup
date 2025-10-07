.PHONY: run install lint type-check pre-commit test coverage all
run:
	@uv run python -m app.main

install:
	@uv sync

lint:
	@uv run ruff check app/ --fix

type-check:
	@uv run pyright app/

pre-commit:
	@uv run pre-commit run --all-files

test:
	@uv run pytest --no-cov

coverage:
	@rm -rf htmlcov .coverage
	@uv run pytest --cov=app --cov-report=term-missing --cov-report=html

all: install lint type-check test

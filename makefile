.PHONY: run install lint type-check pre-commit all
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

all: install lint type-check pre-commit

.PHONY: run install fmt type-check all
run:
	@uv run python -m app.main

install:
	@uv sync

fmt:
	@uv run ruff check . --fix
	@uv run ruff format .

type-check:
	@uv run pyright .

all: install fmt type-check

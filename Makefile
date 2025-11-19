PACKAGE ?= fastup
MAKEFLAGS += --no-print-directory

.PHONY: all run install fmt lint type-check
all: install fmt lint type-check
	@echo "-> ready to go!"

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
	@echo "-> type checking (pyright)"
	@uv run pyright fastup


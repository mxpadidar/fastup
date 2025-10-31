PACKAGE ?= fastup

.PHONY: run install

run:
	@uv run python -m $(PACKAGE).main

install:
	@echo "-> syncing dependencies"
	@uv sync

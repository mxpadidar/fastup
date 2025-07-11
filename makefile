.PHONY: run install test lint type-check all clean tree
run:
	@uv run python -m fastup.main

test:
	@uv run pytest tests --cov=fastup

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

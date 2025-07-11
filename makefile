.PHONY: run install test lint type-check all clean tree
run:
	@uv run python -m fastup.main

install:
	echo "installing dependencies..."
	@uv sync

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

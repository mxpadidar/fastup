.PHONY: runserver install test lint type-check 
runserver:
	@uv run python -m fastup.app

install:
	@uv sync

test:
	@uv run pytest tests/

lint:
	@uv run ruff check fastup/ tests/ --fix

type-check:
	@uv run pyright fastup/ tests/

.PHONY: all clean tree
all: test lint type-check

clean:
	@for name in __pycache__ .cache .venv; do \
		echo "Deleting $$name..."; \
		find . -name "$$name" -exec rm -rf {} + ;\
	done

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv"

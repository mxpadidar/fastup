HOST = 0.0.0.0
PORT = 8000

run:
	uv run uvicorn fastup.main:app --host $(HOST) --port $(PORT) --reload

install:
	uv sync

lint:
	uvx ruff check fastup/ tests/ --fix

typecheck:
	uvx pyright fastup/ tests/

test:
	uv run pytest tests/

check: lint typecheck test

tree:
	@tree -a --dirsfirst -I "__pycache__|.git|.cache|.venv"

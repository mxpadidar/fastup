# FastUp

A minimal FastAPI project scaffold with TOML-based configuration and essential development tooling.

## Requirements

- Python 3.13
- [`uv`](https://github.com/astral-sh/uv)

## Setup

1. Copy the environment example file:

   ```bash
   cp .env.example .env
   ```

2. Install dependencies:

   ```bash
   make install
   ```

## Running the App

```bash
make run-server
```

The app will start at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Development Commands

- Run tests: `make test`
- Lint code: `make lint`
- Type check: `make typecheck`
- Clean project files: `make clean`
- View directory tree: `make tree`

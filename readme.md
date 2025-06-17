# FastUp

A minimal FastAPI project scaffold with TOML-based configuration, database setup, and essential development tooling.

## Requirements

- Python 3.13
- [`uv`](https://github.com/astral-sh/uv)
- [`podman`](https://podman.io/) (for database container)

## Setup

1. Copy the environment file:

   ```bash
   cp .env.example .env
   ```

2. Install dependencies:

   ```bash
   make install
   ```

3. Start the PostgreSQL database:

   ```bash
   make run-db
   ```

   > This will spin up a Podman container using environment variables defined in `.env`.

## Run the App

```bash
make run-server
```

The app will be available at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Development Commands

- Run tests: `make test`
- Lint code: `make lint`
- Type check: `make typecheck`
- Access database CLI: `make psql`
- Stop database container: `make stop-db`
- Remove database container: `make remove-db`
- Clean project files and DB container: `make clean`
- View directory tree: `make tree`

# FastUp

A minimal, versioned FastAPI project scaffold with TOML-based configuration and basic tooling.

## Run the App

```bash
make run
```

The app starts at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Install Dependencies

```bash
make install
```

Uses [`uv`](https://github.com/astral-sh/uv) for fast, modern Python dependency management.

## Create PostgreSQL Container

```bash
make db-up
```

This command uses `Podman` to create a PostgreSQL container.

## Code Quality

Run all checks (lint, typecheck, tests):

```bash
make check
```

## Run Tests

```bash
make test
```

## Requirements

- Python 3.13
- [`uv`](https://github.com/astral-sh/uv)

# fastup

a fastapi starter kit designed to help you build scalable apis quickly.  
it follows best practices and has a clean project structure to jumpstart your development.

## features

- clean, modular project layout
- async sqlalchemy with postgresql via `asyncpg`
- podman-based local postgresql setup
- integrated dev tools (e.g., testing, linting)
- follows fastapi best practices

## database setup

fastup uses postgresql with sqlalchemy (async) for data persistence.  
a lightweight development setup is provided using **podman** (docker alternative).

**makefile targets:**

```bash
make db-up      # start the database container
make db-down    # stop the container
make db-clean   # stop and remove the container and its data
```

> requires a `.env` file with database credentials (see `.env.example`).
> data is stored in `.cache/db-data`.

## 🪪 license

[mit](license)

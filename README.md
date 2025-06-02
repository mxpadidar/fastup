# FastUp

A minimal, versioned FastAPI project scaffold with TOML-based configuration and basic tooling.

## 🚀 Run the App

```bash
make run
````

The app starts at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## ⚙️ Install Dependencies

```bash
make install
```

Uses [`uv`](https://github.com/astral-sh/uv) for fast, modern Python dependency management.

## ✅ Code Quality

Run all checks (lint, typecheck, tests):

```bash
make check
```

## 🧪 Run Tests

```bash
make test
```

## 🐍 Requirements

* Python 3.13
* [`uv`](https://github.com/astral-sh/uv)


## 🔧 Config

App settings are in `config.toml`:

```toml
[fastup]
version = "1.0.0"
port = 8000
```

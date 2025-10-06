# fastup

a minimal yet powerful fastapi starter kit to launch production-ready apis with ease.
built for developers who want clarity, speed, and a solid foundation—without the boilerplate.

## features

- clean, modular project structure
- powered by [`uv`](https://github.com/astral-sh/uv) for fast dependency management
- comprehensive development tooling:
  - **ruff** for linting and formatting
  - **pyright** for type checking
  - **pre-commit** hooks for code quality
  - **makefile** for common development tasks

## development

### setup

```bash
# install dependencies
make install

# install pre-commit hooks
pre-commit install
```

### commands

```bash
make run # run the application
make lint # lint and format code
make type-check # type checking
make pre-commit # run pre-commit hooks
make all # run all checks
```

## License

[MIT](LICENSE)

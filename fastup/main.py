import uvicorn
from fastapi import FastAPI

from fastup.entrypoints.routes import router

app = FastAPI()

app.include_router(router)


def main() -> None:
    """main entry point for the fastapi application."""
    uvicorn.run("fastup.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fastup.core.settings import database_dsn, debug

engine = create_engine(url=database_dsn, echo=debug)

session_maker = sessionmaker(bind=engine)


def get_db() -> Generator[Session]:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()

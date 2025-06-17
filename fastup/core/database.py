from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from fastup.core import settings

url = URL.create(
    "postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)


engine = create_engine(url=url, pool_pre_ping=True, pool_size=20)

session_maker = sessionmaker(bind=engine)

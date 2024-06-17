from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

SQLALCHEMY_DATABASE_URL_POSTGRES = settings.SQLALCHEMY_DATABASE_URL_POSTGRES

# engine_pg_async = create_engine(
#     SQLALCHEMY_DATABASE_URL_POSTGRES
# )
engine_pg_async = create_async_engine(
    SQLALCHEMY_DATABASE_URL_POSTGRES
)

# SessionPGAsync = sessionmaker(autocommit=False, autoflush=False, bind=engine_pg_async)
SessionPGAsync = AsyncSession(engine_pg_async)

BasePgAsync = declarative_base()

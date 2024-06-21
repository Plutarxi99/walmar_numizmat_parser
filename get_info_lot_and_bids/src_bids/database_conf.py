from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL_SQLITE_FOR_BIDS

engine_bids = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionBids = sessionmaker(bind=engine_bids)

BaseBids = declarative_base()

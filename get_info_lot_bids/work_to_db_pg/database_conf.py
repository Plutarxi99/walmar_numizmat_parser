from sqlalchemy import create_engine, Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL_POSTGRES_SHORT

engine_html_str = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionHtmlStr = sessionmaker(bind=engine_html_str)

Base = declarative_base()


class HtmlStr(Base):
    __tablename__ = "html_str"

    id = Column(Integer, primary_key=True, index=True)
    html = Column(TEXT)
    id_auction_hidden = Column(Integer)
    # id_hidden_lot = Column(Integer, unique=True)
    id_lot_hidden = Column(Integer)

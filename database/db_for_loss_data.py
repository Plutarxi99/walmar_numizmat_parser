from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL_LOSS

engine_loss = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocalLoss = sessionmaker(autocommit=False, autoflush=False, bind=engine_loss)

Base_loss = declarative_base()


class LotAuctionLoss(Base_loss):
    __tablename__ = 'lot_action'

    lot_id = Column(Integer, primary_key=True)
    id_lot_hidden = Column(Integer)
    id_auction_hidden = Column(Integer)

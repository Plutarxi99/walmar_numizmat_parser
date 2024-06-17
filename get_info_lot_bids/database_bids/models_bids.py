from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from config import settings
from get_info_lot_bids.database_bids.bd_bids import BasePgAsync


class Bids(BasePgAsync):
    __tablename__ = settings.POSTGRES_TABLE

    id = Column(Integer, primary_key=True, index=True)
    id_hidden_lot = Column(Integer, unique=True)
    amount_bid = Column(Integer)
    nickname = Column(String(150))
    datetime_pay = Column(String(60))




from sqlalchemy import Column, Integer, String
from config import settings
from get_info_auction_and_lot.src_auction.db import Base


class LotAuction(Base):
    __tablename__ = settings.NAME_TABLE

    lot_id = Column(Integer, primary_key=True)
    title_lot = Column(String(250))
    year_coin = Column(Integer, nullable=True)
    mint = Column(String(30), nullable=True)
    metal_gr = Column(String(30), nullable=True)
    safety = Column(String(30), nullable=True)
    buyer = Column(String(50), nullable=True)
    bids = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)
    status = Column(String(30), nullable=True)
    type_auction = Column(String(10), nullable=True)
    id_auction_hidden = Column(Integer) # qwe
    id_auction_visible = Column(Integer)
    id_lot_hidden = Column(Integer) # qwe
    date_closed = Column(String)
    # type_category = Column(String(100), nullable=True)
    full_url = Column(String(150), unique=True)
# [('15 рублей !', '1897', 'АГ', 'Au', 'XF', 'Sega269', '10', '14858', 'Закрыто',
# 'vip', ['1553'], '11', ['33'], '14.12.2006 12:00', 'https://www.wolmar.ru/auction/33/1553')
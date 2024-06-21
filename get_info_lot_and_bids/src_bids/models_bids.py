from get_info_lot_and_bids.src_bids.database_conf import BaseBids
from sqlalchemy import Column, Integer, TEXT


class HtmlStr(BaseBids):
    __tablename__ = "html_str"

    id = Column(Integer, primary_key=True, index=True)
    html = Column(TEXT)
    id_auction_hidden = Column(Integer)
    id_lot_hidden = Column(Integer)

from bs4 import BeautifulSoup

from database import models
from database.db import SessionLocal, engine
from database.models import LotAuction

from get_info_lot_bids.get import get_data_from_page_pass_test


def get_soup(data):
    soup = BeautifulSoup(data, 'lxml')
    return soup


def get_lot_id(id_auction_hidden):
    with (SessionLocal() as session):
        res = session.query(LotAuction.id_auction_hidden,
                            LotAuction.id_lot_hidden,
                            ).values()
        # .filter(
        #     LotAuction.id_auction_hidden == id_auction_hidden
        # )
        print(res)
        # for x in res:
        #     print(x.lot_id)


def get_clear_data(soup):
    # https://www.wolmar.ru/ajax/bids.php?auction_id=1983&lot_id=6734542
    pass


data = get_data_from_page_pass_test()
soup = get_soup(data)
# print(data)
print(get_lot_id(31))

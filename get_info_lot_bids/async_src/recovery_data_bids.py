from sqlalchemy.dialects.postgresql import psycopg2

from config import settings
from database.db import SessionLocal
from database.models import LotAuction


def get_list_id_lots_on_auction_referens(id_action):
    """
    Возвращает список всех лотов по аукиону
    :param id_action:
    :return: [5345345, 2535235, 235235]
    """
    with SessionLocal() as session:
        r = [x.id_lot_hidden for x in session.query(LotAuction.id_auction_hidden,
                                                    LotAuction.id_lot_hidden, ).filter(
            LotAuction.id_auction_hidden == id_action).distinct()]
    return r


def get_list_id_lots_on_auction_lie(id_action):
    """

    :param id_action:
    :return:
    """
    connection = psycopg2.connect(settings.SQLALCHEMY_DATABASE_URL_POSTGRES_SHORT)
    with connection as conn:
        list_lots = conn.execute(
            """SELECT id_lot_hidden, id_auction_hidden from html_str where id_auction_hidden=1987""")
    return list_lots


print(get_list_id_lots_on_auction_lie(1987))

import psycopg2

from config import settings
from database.db import SessionLocal
from database.db_for_loss_data import SessionLocalLoss, Base_loss, engine_loss
from database.models import LotAuction


def add_row_loss_lot(row):
    with SessionLocalLoss() as session:
        # session.bulk_insert_mappings(LotAuction, row)
        session.bulk_insert_mappings(LotAuction, row)
        session.commit()


def get_id_auction_lie_in_db(table):
    """
    возвращает не повторяющиеся элементы аукциона в в таблице
    :param table:
    :return: [1987, 1986, 1985, 1984, 1983, 1982, 1980, 1979, 1978, 1977]
    """
    connection = psycopg2.connect(
        host=settings.POSTGRES_SERVER,
        database='walmart_coin_2',
        port=5432,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )
    with connection.cursor() as conn:
        conn.execute(
            f"""SELECT DISTINCT id_auction_hidden from {table} ORDER BY id_auction_hidden DESC """)
        list_auction = [row[0] for row in conn.fetchall()]
    return list_auction


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


def get_list_id_lots_on_auction_lie(id_action, table_in_db):
    """

    :param id_action:
    :return:
    """
    # connection = psycopg2.connect(settings.SQLALCHEMY_DATABASE_URL_POSTGRES_SHORT)
    connection = psycopg2.connect(
        host=settings.POSTGRES_SERVER,
        database='walmart_coin_2',
        port=5432,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )
    with connection.cursor() as conn:
        conn.execute(
            f"""SELECT id_lot_hidden from {table_in_db} where id_auction_hidden={id_action}""")
        list_lots = [row[0] for row in conn.fetchall()]
    return list_lots


# print(get_list_id_lots_on_auction_lie(1987))
# print(get_list_id_lots_on_auction_referens(1987))
def main(id_auction, table_in_db):
    list_ref = get_list_id_lots_on_auction_referens(id_auction)
    list_lie = get_list_id_lots_on_auction_lie(id_auction, table_in_db)
    set_ref = set(list_ref)
    set_lie = set(list_lie)
    diff_set = set_ref.difference(set_lie)
    # diff_set = set_ref - set_lie
    return list(diff_set)


if __name__ == "__main__":
    # создаем базу данных и содержащихся в них таблицы
    Base_loss.metadata.create_all(bind=engine_loss)
    table_in_db = 'html_str'
    list_id_auc = get_id_auction_lie_in_db(table_in_db)
    for id_auc in list_id_auc:
        res = [{'id_lot_hidden': sub, "id_auction_hidden": id_auc} for sub in main(id_auc, table_in_db)]
        print(res)
        if res != []:
            add_row_loss_lot(res)
        print("Готово")
    # a = [(6757894, 12), (6757894, 2)]
    # a = [{'id_lot_hidden': 6757894, "id_auction_hidden": 1986}, {'id_lot_hidden': 6757894, "id_auction_hidden": 1986}]
    # add_row_loss_lot(a)

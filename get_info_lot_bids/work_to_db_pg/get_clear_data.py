import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from selectolax.lexbor import LexborHTMLParser

from config import settings
from get_info_lot_bids.work_to_db_pg.database_conf import engine_html_str, HtmlStr, SessionHtmlStr


def get_html_str():
    with SessionHtmlStr() as session:
        # for html in session.query(HtmlStr).all():
        #     print(html.id_lot_hidden)
        res = session.query(HtmlStr).filter(HtmlStr.id_lot_hidden == 6767664).all()
    return res[0].html


def parser_selectolax(data):
    parser = LexborHTMLParser(data)

    # Найдите таблицу и извлеките данные в список списков
    table = parser.css_first('table')
    rows = [[td.text() for td in tr.css('td')] for tr in table.css('tr')[1:]]

    # Создайте список со значениями таблиц
    table_values = []
    for row in rows:
        amount_bid = int(row[0].replace(' ', ''))
        nickname = row[2]
        datetime_pay = row[3]
        table_values.append({'amount_bid': amount_bid, 'nickname': nickname, 'datetime_pay': datetime_pay})

    return table_values
print(parser_selectolax(get_html_str()))
# print(get_html_str())

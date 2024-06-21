import time
from pathlib import Path

import psycopg2
import csv
from selectolax.lexbor import LexborHTMLParser
from sqlalchemy import select

from config import settings
from get_info_lot_and_bids.src_bids.database_conf import SessionBids
from get_info_lot_and_bids.src_bids.models_bids import HtmlStr

count_loss_bad_request = 0
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def write_in_csv(data) -> None:
    """
    Запись в csv файл из бд postgresql
    :param data: TODO: дополнить данные
    :return: None
    """
    with open(BASE_DIR / 'bids_csv.csv', 'w', newline='') as filename:
        write_filename = csv.writer(filename, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        column_names = ['id', 'id_hidden_auction', 'id_hidden_lot', 'amount_bid', 'nickname', 'datetime_pay', 'status']
        write_filename.writerow(column_names)
        for bid in data:
            list_value = list(bid.values())
            write_filename.writerow(list_value)


def parser_selectolax(data):
    """
    Быстрый парсер. Быстрее используемого ранее BeatifualSoup4. У меня вышла разница в 14 раз
    :param data: html страницы находиться пример по адресу get_info_lot_bids/data/lot1.html
    :return: TODO: дополнить данные
    """
    global count_loss_bad_request
    parser = LexborHTMLParser(data)
    try:
        table = parser.css_first('table')
        rows = [[td.text() for td in tr.css('td')] for tr in table.css('tr')[1:]]

        status_choise = {'first': 'first', 'inter': 'inter', 'final': 'final'}
        table_values = []
        count_number_buyer = 0
        all_records_in_list = len(rows)
        for row in rows:
            amount_bid = str(int(row[0].replace(' ', '')))
            nickname = row[2]
            datetime_pay = row[3]
            res = {'amount_bid': amount_bid, 'nickname': nickname, 'datetime_pay': datetime_pay}
            if (all_records_in_list - count_number_buyer) == all_records_in_list:
                res['status'] = status_choise['final']
            elif (all_records_in_list - 1) == count_number_buyer:
                res['status'] = status_choise['first']
            else:
                res['status'] = status_choise['inter']
            table_values.append(res)
            count_number_buyer += 1
        return table_values
    except Exception as e:
        count_loss_bad_request += 1
        print(count_loss_bad_request)
        return None


def get_data_in_db(a, b, table_name, type_work):
    """
    Получение данных из бд postgresql ввиде списка
    :return: TODO: дополнить данные
    """
    if type_work == "sqllite3":
        with SessionBids() as session:
            if a != b:
                # res = session.query(HtmlStr).filter(HtmlStr.id_auction_hidden.between(a, b)).all()
                # res = session.query(HtmlStr).filter(HtmlStr.id_auction_hidden.between(a, b)).first()
                res = [(x.id, x.html, x.id_lot_hidden, x.id_auction_hidden) for x in
                       session.query(HtmlStr).filter(HtmlStr.id_auction_hidden.between(a, b)).all()]
            else:
                res = session.query(HtmlStr).filter(HtmlStr.id_auction_hidden == a).all()
            return res
    else:
        conn = psycopg2.connect(dbname=settings.POSTGRES_DB, user=settings.POSTGRES_USER,
                                password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_SERVER)

        cursor = conn.cursor()
        cursor.execute(
            f'SELECT  * FROM {table_name} WHERE id_auction_hidden BETWEEN {a} AND {b} ORDER BY id_lot_hidden DESC;')
        list_data = []
        for row in cursor:
            list_data.append(row)
        cursor.close()
        conn.close()
        return list_data


def main(id_auction_less, id_auction_greater, table_name_ib_db, type_work):
    step = (id_auction_less, id_auction_greater)
    start_time = time.time()
    data = get_data_in_db(a=step[0], b=step[1], table_name=table_name_ib_db, type_work=type_work)
    list_clear_data = []
    for html_str in data:
        clear_data = parser_selectolax(html_str[1])
        if clear_data is not None:
            for number_index in range(len(clear_data)):
                list_clear_data_str = list(
                    clear_data[number_index].items())  # получение ключа и значений ввиде пар кортежей ввиде списка
                list_clear_data_str.insert(0, (
                    'id_hidden_lot', str(html_str[2])))  # меняем места для более красивого отображения данных в csv
                list_clear_data_str.insert(0, ('id_hidden_auction', str(html_str[3])))
                list_clear_data_str.insert(0, ('id', str(html_str[0])))
                list_clear_data.append(dict(list_clear_data_str))

    write_in_csv(list_clear_data)
    print(f"Записано {step}")
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    id_auction_less = 1987
    id_auction_greater = 1989
    table_name_ib_db = "html_str"
    type_work = settings.TYPE_WORK
    main(id_auction_less, id_auction_greater, table_name_ib_db, type_work)

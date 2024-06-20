import time
import psycopg2
import csv
from selectolax.lexbor import LexborHTMLParser

from config import settings
count = 0
# утратила свою полезность
def swap_in_list(list_value, a, b):
    tmp_a = list_value[a]
    list_value[a] = list_value[b]
    list_value[b] = tmp_a
    return list_value


def write_in_csv(data) -> None:
    """
    Запись в csv файл из бд postgresql
    :param data: TODO: дополнить данные
    :return: None
    """
    with open('bids_csv.csv', 'w', newline='') as filename:
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
    global count
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
        count += 1
        print(count)
        return None


def get_data_in_db():
    """
    Получение данных из бд postgresql ввиде списка
    :return: TODO: дополнить данные
    """
    conn = psycopg2.connect(dbname=settings.POSTGRES_DB, user=settings.POSTGRES_USER,
                            password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_SERVER)

    cursor = conn.cursor()
    # cursor.execute(f'select * from {settings.NAME_TABLE_HTML};')
    # cursor.execute(f'-- SELECT * FROM {settings.NAME_TABLE_HTML} WHERE id_auction_hidden BETWEEN 1478 AND 1484;')
    # cursor.execute(f'SELECT * FROM {settings.NAME_TABLE_HTML} WHERE id_auction_hidden=1438;')
    # cursor.execute(f'-- SELECT * FROM html_str_2 WHERE id_auction_hidden BETWEEN 1294 AND 1298;')
    # cursor.execute(f'-- SELECT * FROM html_str_2 WHERE id_auction_hidden=1053;')
    cursor.execute(f'SELECT * FROM html_str_3 WHERE id_auction_hidden BETWEEN 666 AND 673;')
    # cursor.execute(f'-- SELECT * FROM html_str_3 WHERE id_lot_hidden=1718470;')
    list_data = []
    for row in cursor:
        list_data.append(row)
    # print(list_data)
    cursor.close()
    conn.close()
    return list_data

def main():
    start_time = time.time()
    data = get_data_in_db()
    list_clear_data = []
    for html_str in data:
        clear_data = parser_selectolax(html_str[1])  # 10000 записей за 1.920641422271728
        if clear_data is not None:
            for number_index in range(len(clear_data)):
                # ord_dict = OrderedDict(clear_data[number_index])
                list_clear_data_str = list(clear_data[number_index].items()) # получение ключа и значений ввиде пар кортежей ввиде списка
                list_clear_data_str.insert(0, ('id_hidden_lot', str(html_str[2]))) # меняем места для более красивого отображения данных в csv
                list_clear_data_str.insert(0, ('id_hidden_auction', str(html_str[3])))
                list_clear_data_str.insert(0, ('id', str(html_str[0])))
                list_clear_data.append(dict(list_clear_data_str))

    write_in_csv(list_clear_data)
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    main()

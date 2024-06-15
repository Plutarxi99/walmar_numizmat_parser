import sqlite3
import sys
from datetime import datetime
import traceback

import sqlalchemy

from config import settings
from database import models
from database.db import engine, SessionLocal
from database.models import LotAuction

from src.get_data import get_data_from_page_pass_test, get_data_from_page
from src.note_finally_parser import push_note_mail
from src.parser_data import get_all_number_auction, get_soup_parser, parser_info_auction, parser_table_info, \
    get_dict_number_auction_type
from src.work_with_last_iter import control_last_iter

if __name__ == "__main__":

    start = datetime.now()
    print(f"Начало парсинга {start}\n")
    # создаем базу данных и содержащихся в них таблицы
    models.Base.metadata.create_all(bind=engine)
    # html_str_static = get_data_from_page_pass_test(
    #     'data_test/res_test.txt')  # получение обычной страницы уже подгруженной в папке
    # soup_static = get_soup_parser(data=html_str_static)  # получаем экзмеляра для парсинга страницы
    list_auction_number_static = get_all_number_auction()  # получаем список id аукционов
    type_auction_dict = get_dict_number_auction_type()  # получаем словарь id аукционов и их типов
    # info_auction_generally_static = parser_info_auction(soup_static)  # получаем название аукционов
    # data_info_lot = parser_table_info(soup)
    last_iter = int(control_last_iter(type_work='start'))
    if last_iter == 0:
        index_last_iter = 0
    else:
        try:
            index_last_iter = list_auction_number_static.index(last_iter)
        except ValueError as e:
            print("Указан не верное id аукциона, который есть в URL, "
                  "либо его не существует, либо не правильная цифра в data_test/log.txt")
            sys.exit()

    print(f"Начало парсинга началось с {index_last_iter}")
    for number_auction in list_auction_number_static[index_last_iter:]:
        control_last_iter(type_work='write', value=str(number_auction))

        # list_category = info_auction_generally_static['category_auction']
        # for category_auction in list_category:
        # https://www.wolmar.ru/auction/1983/monety-antika-srednevekove
        # url_on_auction = settings.URL_DOMEN + '/auction/' + number_auction + '/' + category_auction + '?all=1'

        url_on_auction = settings.URL_DOMEN + '/auction/' + str(number_auction) + '?all=1'
        html_str = get_data_from_page(url_on_auction)
        # if html_str is None:
        #     sys.exit("Проблема в получении данных")
        soup = get_soup_parser(data=html_str)
        info_auction_generally = parser_info_auction(soup)
        data_closed = info_auction_generally['date_closed']
        id_auction_visible = info_auction_generally['id_auction_visible']
        type_auction = type_auction_dict[number_auction]
        data_info_lot = parser_table_info(soup, date_closed=data_closed,
                                          id_auction_visible=id_auction_visible,
                                          type_auction=type_auction)

        print(f"Записываем в базу данных {info_auction_generally['title_auction']}")

        with SessionLocal() as session:
            try:
                res = session.bulk_insert_mappings(LotAuction, data_info_lot)
                session.commit()
                print(
                    f"Конец обработки страницы аукциона {info_auction_generally['title_auction']} -- {datetime.now()}\n"
                    f"*******************************************")
            except Exception as e:
                # except sqlite3.IntegrityError as e:
                # except (sqlalchemy.exc.IntegrityError, sqlite3.IntegrityError, ) as e:
                # except (sqlalchemy.exc.IntegrityError, sqlite3.IntegrityError, ) as e:
                now = datetime.now()
                text_error = f"Ошибка обработана и записана в логи время: Проблема с записью в базу данных {now}"
                print(text_error)
                where_problem = 'LotAuction.insert_many(data_info_lot).execute()'
                cannot_write = info_auction_generally['title_auction']
                info_log = f'[{now}] -- [{where_problem}] -- [Не смог записать аукцион с названием {cannot_write}; url: {url_on_auction}] -- [{e}] -- [{traceback.format_exc()}]\n'
                with open("data_test/log.txt", 'a') as txt:
                    txt.write(info_log)
                push_note_mail(email_text=text_error, subject_email="Проблема с записью базы данных")
                # continue

    time_work = f"Парсинг окончен {datetime.now() - start}"
    print(time_work)
    push_note_mail(email_text=time_work, subject_email="Время работы парсера")

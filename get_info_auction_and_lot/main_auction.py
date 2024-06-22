import sys
from datetime import datetime
import traceback
from os.path import dirname, abspath
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from config import settings

from get_info_auction_and_lot.src_auction import models
from get_info_auction_and_lot.src_auction.db import engine, SessionLocal
from get_info_auction_and_lot.src_auction.get_data import get_data_from_page
from get_info_auction_and_lot.src_auction.models import LotAuction
from get_info_auction_and_lot.src_auction.parser_data import get_all_number_auction, get_dict_number_auction_type, \
    get_soup_parser, parser_info_auction, parser_table_info
from get_info_auction_and_lot.src_auction.work_with_last_iter import control_last_iter, get_path_to_file_log
from note_finally_parser import push_note_mail

if __name__ == "__main__":

    start = datetime.now()
    print(f"Начало парсинга {start}\n")
    # создаем базу данных и содержащихся в них таблицы
    models.Base.metadata.create_all(bind=engine)
    list_auction_number_static = get_all_number_auction()  # получаем список id аукционов
    type_auction_dict = get_dict_number_auction_type()  # получаем словарь id аукционов и их типов
    last_iter = int(control_last_iter(type_work='start'))
    # блок для запуска проверки и создания файла с последней итерацией
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
        # записываем итерируемый аукцион
        control_last_iter(type_work='write', value=str(number_auction))
        # создаем url на который будем обращаться
        url_on_auction = settings.URL_DOMEN + '/auction/' + str(number_auction) + '?all=1'
        # делаем запрос к url
        html_str = get_data_from_page(url_on_auction)
        # получение объекта soup для получение таблицы
        soup = get_soup_parser(data=html_str)
        # получение со страницы названия, закрытие и состояние аукциона
        info_auction_generally = parser_info_auction(soup)
        # берем полученные данные для составление результирующего ответа
        data_closed = info_auction_generally['date_closed']
        id_auction_visible = info_auction_generally['id_auction_visible']
        type_auction = type_auction_dict[number_auction]
        # получение данных по каждому лоту
        data_info_lot = parser_table_info(soup, date_closed=data_closed,
                                          id_auction_visible=id_auction_visible,
                                          type_auction=type_auction)

        print(f"Записываем в базу данных {info_auction_generally['title_auction']}")
        # открываем соединение и записываем в бд полученные данные
        with SessionLocal() as session:
            try:
                res = session.bulk_insert_mappings(LotAuction, data_info_lot)
                session.commit()
                print(
                    f"Конец обработки страницы аукциона {info_auction_generally['title_auction']} -- {datetime.now()}\n"
                    f"*******************************************")
            except Exception as e:
                now = datetime.now()
                text_error = f"Ошибка обработана и записана в логи время: Проблема с записью в базу данных {now}"
                print(text_error)
                where_problem = 'LotAuction.insert_many(data_info_lot).execute()'
                cannot_write = info_auction_generally['title_auction']
                info_log = f'[{now}] -- [{where_problem}] -- [Не смог записать аукцион с названием {cannot_write}; url: {url_on_auction}] -- [{e}] -- [{traceback.format_exc()}]\n'
                path_to_file_log = get_path_to_file_log()
                with open(path_to_file_log, 'a') as txt:
                    txt.write(info_log)
                push_note_mail(email_text=text_error, subject_email="Проблема с записью базы данных")

    time_work = f"Парсинг окончен {datetime.now() - start}"
    print(time_work)
    # отправка уведомления об окончании парснга
    push_note_mail(email_text=time_work, subject_email="Время работы парсера")

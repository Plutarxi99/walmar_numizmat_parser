import random
import sys
from datetime import datetime
from http import HTTPStatus

import requests

from get_info_auction_and_lot.help_for_request_auction.list_headers import get_random_headers_auction
from get_info_auction_and_lot.src_auction.work_with_last_iter import get_path_to_file_log
from note_finally_parser import push_note_mail


def get_data_from_page(url: str = "https://www.wolmar.ru/auction/1251"):
    """
    Получение данных с указанной страницы
    :param url: https://www.wolmar.ru/auction/1251
    :return: str в виде html страницы
    """
    headers = get_random_headers_auction()
    res = requests.get(url, headers=headers)
    if res.status_code == HTTPStatus.OK:
        start = datetime.now()
        print(f"Начало обработки страницы аукциона {start}")
        print(f"Получение данных из источника {url}")
        return res.text
    else:
        now = datetime.now()
        text_error = f"Ошибка обработана и записана в логи время: {now}"
        print(text_error)
        where_problem = 'requests.get(url, headers=list_headers...'
        info_log = f'[{now}] -- [Проблема в получении ответа от запроса {where_problem}] -- [src.get_data.get_data_from_page] -- [{headers}]\n'
        path_to_file_log = get_path_to_file_log()
        with open(path_to_file_log, 'a') as txt:
            txt.write(info_log)
        push_note_mail(email_text=text_error, subject_email="Проблема с получением страницы html")
        sys.exit()

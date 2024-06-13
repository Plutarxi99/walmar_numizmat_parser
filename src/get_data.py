import random
from datetime import datetime
from time import sleep

import requests


def get_data_from_page_pass_test(url: str = '../data_test/res_test.txt'):
    """
    Заглушка. Служит для получения html страницы без обращения к адресу сайта
    :type url: str по дефолту стоит заглушка из текстового файла полученный путем запроса html страница
    :return: текст html страницы
    """
    text_res = ""
    with open(url, "r") as res:
        # with open("../data_test/test_history_auction_all_page_text.txt", "r") as res:
        text_res = res.read()
    return text_res


def get_data_from_page(url: str = "https://www.wolmar.ru/auction/1251"):
    """
    Получение данных с указанной страницы
    :param url: https://www.wolmar.ru/auction/1251
    :return: str в виде html страницы
    """
    # https://www.wolmar.ru/auction/1980?all=1 - показать все монеты
    # https://www.wolmar.ru/auction/1980 - показать только первую страницу
    list_headers = [
        {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.750 Yowser/2.5 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36/537.36"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:125.0) Gecko/20100101 Firefox/125.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:125.0) Gecko/20100101 Firefox/125.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:124.0) Gecko/20100101 Firefox/124.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:124.0) Gecko/20100101 Firefox/124.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    ]
    headers = list_headers[random.randint(0, 15)]
    res = requests.get(url, headers=headers)
    sleep(random.randint(10, 20))
    if res.status_code == 200:
        print(f"Получение данных из источника {url}")
        return res.text
    else:
        now = datetime.now()
        print(f"Ошибка обработана и записана в логи время: {now}")
        where_problem = 'requests.get(url, headers=list_headers...'
        info_log = f'[{now}] -- [Проблема в получении ответа от запроса {where_problem} ] -- [src.get_data.get_data_from_page] -- [{headers}]\n'
        with open("../data_test/log.txt", 'a') as txt:
            txt.write(info_log)
        return None

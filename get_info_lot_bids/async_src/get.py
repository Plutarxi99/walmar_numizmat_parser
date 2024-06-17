import asyncio
import datetime

import sys
import traceback
from http import HTTPStatus

import aiohttp
import logging

from aiohttp.web_exceptions import HTTPError

from get_info_lot_bids.async_src.as_pg_async_write_html import add_html_str_pg_asyncpg

from get_info_lot_bids.async_src.func import make_url_for_get_data_async, get_lot_id_async, \
    get_diff_for_equally_async
from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction
from get_info_lot_bids.async_src.help_for_request.list_proxies import get_proxies
from get_info_lot_bids.async_src.help_for_request.list_user_agent import get_headers
from src.note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


async def get_page_data(id_auction, left_slice, right_slice, list_id_lot):
    for id_lot in list_id_lot[left_slice:right_slice]:
        url = await make_url_for_get_data_async(id_auction, id_lot)
        # proxy_url = 'https://papaproxy.net/api/getproxy/?r=1&format=txt&type=http_ip&login=RUSHE479U2&password=TviZ4Ak2'
        proxy = await get_proxies()
        try:
            headers = await get_headers()
            async with aiohttp.ClientSession() as session:
                # proxy = await session.get(url=proxy_url, headers=headers)
                response = await session.get(url=url, headers=headers, proxy=proxy)
                # response = await session.get(url=url, headers=headers, proxies=proxies)
                # response = await session.get(url=url, headers=headers)
                if response.status == HTTPStatus.OK:
                    response_text = await response.text()
                    await add_html_str_pg_asyncpg(html=response_text, id_lot_hidden=id_lot,
                                                  id_auction_hidden=id_auction)
                    print(f"Отработан аукцион {id_auction}\n"
                          f"Отработан лот {id_lot}\n")
                else:
                    date_wrong = datetime.datetime.now()
                    logging.error(f"[{date_wrong}]"
                                  f"Возбуждено исключение на запрос к сервису"
                                  f"Ошибка при за запросе. Статус кода: {response.status}"
                                  f"Текст запроса: {response.text()}"
                                  f"{url}"
                                  f"{proxy}"
                                  f"===============================================")
                    with open("last_url.txt", 'a') as t:
                        t.write(f"{url}\n")
                    # raise HTTPError()

        except Exception as e:
            date_wrong = datetime.datetime.now()
            logging.error(f"[{date_wrong}]"
                          f"Проблема в получении запроса {e}"
                          f"url запроса <{url}>"
                          f"proxy <{proxy}>"
                          f"{traceback.format_exc()}"
                          f"===============================================")
            push_note_mail(email_text=f"Упала ошибка. Проблема в получении данных {e}",
                           subject_email="Проблема с таблицей платежей лотов")
            sys.exit()


async def gather_data(count_create_task, list_id_auction):
    tasks = []
    # count_create_task = 5 # minimum working
    # count_create_task = 2 на 50 аукционов тяжело с просадками
    # 5 воркеров на 50 данных много

    # ошибка 500 //// 2 воркера \\\\ на 50 задча \\\\ через 1:30 часа \\\\
    # ***** здесь была ошибка list_id_hidden_auction[5:50] не полные данные
    # count_create_task = 2  # minimum working
    # past_i_want_auction = 5
    # get_i_want_auction = 50
    # *****
    # ***** удачно
    # count_create_task = 5  # minimum working
    # past_i_want_auction = 50
    # get_i_want_auction = 55
    # ***** Good
    # count_create_task = 5
    # past_i_want_auction = 55
    # get_i_want_auction = 60
    # ***** 5 / 60 / 65
    # ***** 5 / 65 / 70
    # ***** 5 / 70 / 75
    # ***** 5 / 75 / 80
    # ***** 3 / 80 / 90
    # ***** 10 /100 / 101
    # count_create_task = 10
    # past_i_want_auction = 100
    # get_i_want_auction = 101
    # list_id_auction = list_id_hidden_auction[past_i_want_auction:get_i_want_auction]
    logging.warning(
        f"\n*************************\nБудут c работать воркерами {count_create_task} загружены эти данные{list_id_auction}\n*************************\n")
    for id_auction in list_id_auction:
        list_id_lot = await get_lot_id_async(id_auction)
        print(f"Получение списка лота для {id_auction}")
        list_slice = await get_diff_for_equally_async(id_auction, count_create_task)
        for slice_border in list_slice:
            task = asyncio.create_task(
                get_page_data(id_auction, slice_border[0], slice_border[1], list_id_lot))
            tasks.append(task)

    await asyncio.gather(*tasks)

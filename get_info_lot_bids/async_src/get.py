import asyncio
import datetime
import random
import sys
import traceback
from http import HTTPStatus

import aiohttp
import logging

from aiohttp.web_exceptions import HTTPError

from config import settings
from get_info_lot_bids.async_src.async_asyncpg import add_record_pg_asyncpg
from get_info_lot_bids.async_src.func import get_clear_data_async, make_url_for_get_data_async, get_lot_id_async, \
    get_auction_id_not_async
from get_info_lot_bids.async_src.help_for_request.list_user_agent import list_headers, get_headers
from src.note_finally_parser import push_note_mail

#     get_auction_id_not_async
# from get_info_lot_bids.async_src.pg_async import add_record_pg

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


# async def get_page_data(id_auction, a, b):
async def get_page_data(id_auction):

    list_id_lot = await get_lot_id_async(id_auction)
    # for id_lot in list_id_lot[a:b]:
    for id_lot in list_id_lot:
        url = await make_url_for_get_data_async(id_auction, id_lot)
        headers = get_headers()
        proxy_ip_def = settings.PROXIES_IP_DEF
        proxy_port_def = settings.PROXIES_PORT_DEF
        proxies = {
            'http': f'http://{proxy_ip_def}:{proxy_port_def}',
            'https': f'http://{proxy_ip_def}:{proxy_port_def}'
        }
        print(f"Создаем url {url}")
        try:
            async with aiohttp.ClientSession() as session:
                # response = await session.get(url=url, headers=headers, proxies=proxies)
                response = await session.get(url=url, headers=headers)
                print(f"Отработан запрос {id_lot}\n")
                if response.status == HTTPStatus.OK:
                    response_text = await response.text()
                    clear_data = await get_clear_data_async(response_text)
                    print(f"Отработана чистка данных {id_lot}\n")
                    # await add_record_pg(data=clear_data, id_hidden_lot=id_lot)
                    # if clear_data is None or clear_data == []:
                    await add_record_pg_asyncpg(data=clear_data, id_hidden_lot=id_lot)
                    print(f"Отработан лот {id_lot}\n")
                else:
                    date_wrong = datetime.datetime.now()
                    logging.error(f"[{date_wrong}]"
                                  f"Возбуждено исключение на запрос к сервису"
                                  f"Ошибка при за запросе. Статус кода: {response.status}"
                                  f"Текст запроса: {response.text()}")
                    raise HTTPError()

        except Exception as e:
            date_wrong = datetime.datetime.now()
            logging.error(f"[{date_wrong}]"
                          f"Проблема в получении запроса {e}"
                          f"{traceback.format_exc()}")
            push_note_mail(email_text=f"Упала ошибка. Проблема в получении данных {e}",
                           subject_email="Проблема с таблицей платежей лотов")
            sys.exit()
        # print(clear_data)
        # print(f"[INFO] Обработал страницу {id_lot}")  # TODO: delete


async def gather_data():
    tasks = []
    # list_id_auction = get_auction_id_not_async()
    list_id_auction = [1985]
    # id_auction = 1985
    for id_auction in list_id_auction:
        task = asyncio.create_task(get_page_data(id_auction))
    # Что возвращает функция, asyncio.create_task(get_page_data(id_auction))<Task pending name='Task-7'
    # coro=<get_page_data() running at /home/egor/PycharmProjects/work/walmar_numizmat_parser/get_info_lot_bids/async_src/get.py:11>>
    # print(f'Что возвращает функция, asyncio.create_task(get_page_data(id_auction)){task}\n') # TODO: delete
        tasks.append(task)

    await asyncio.gather(*tasks)

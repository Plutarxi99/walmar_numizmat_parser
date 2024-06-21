import asyncio

import aiohttp
import logging

from get_info_lot_and_bids.src_bids.as_pg_async_write_html import add_html_str_pg_asyncpg

from get_info_lot_and_bids.src_bids.func import make_url_for_get_data_async, get_lot_id_async, \
    get_diff_for_equally_async
# from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction # TODO: раскоммитить
from get_info_lot_and_bids.help_for_request_bids.get_proxies import get_proxies
from get_info_lot_and_bids.help_for_request_bids.get_headers import get_headers

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")
logging.error("get_file")


async def get_page_data(id_auction, left_slice, right_slice, list_id_lot, type_work):
    data_req = [] # заполняем список для полученных результатов
    for id_lot in list_id_lot[left_slice:right_slice]:  # идём по циклу получаем срез списка, указанный ранее
        url = await make_url_for_get_data_async(id_auction, id_lot)  # получаем url
        proxy = await get_proxies()  # получаем случаный прокси-сервер(заранее заготовленный список, можно получать по url случайный ip)
        try:
            headers = await get_headers()  # получаем случайный заголовок(возможно избегает блокировку)
            async with aiohttp.ClientSession() as session:
                if proxy is None:
                    response = await session.get(url=url, headers=headers)
                else:
                    response = await session.get(url=url, headers=headers, proxy=proxy)
                if response.status == 200:
                    response_text = await response.text()  # запрос превращаем текста для дальнейшего парсинга

                    tuple_data = (response_text, id_lot, id_auction)
                    data_req.append(tuple_data)
                else:
                    logging.error(f"[date_wrong]"
                                  f"Возбуждено исключение на запрос к сервису"
                                  f"{url}"
                                  f"{proxy}"
                                  f"===============================================")
        # отлов ошибки (интересная штука, что-то возбуждает исключение, что прокси в запросе не работает,
        # но по факту работает и запрос проходит успешно.
        # Также запрашиваемые данные успешно отсылаются) Поэтому, я после этой ошибки записываю данные в бд
        except aiohttp.client_exceptions.ClientProxyConnectionError as e:
            try:
                if response.status == 200:
                    tuple_data = (response_text, id_lot, id_auction)
                    data_req.append(tuple_data)
                elif response.status == 500:
                    tuple_data = (response_text, id_lot, id_auction)
                    data_req.append(tuple_data)
                else:
                    print(f"ClientProxyConnectionError | "
                          f"status = {response.status} | "
                          f"{e} | "
                          "Уходит в сон")
                    continue
            except UnboundLocalError as e:
                print(f"ClientProxyConnectionError | UnboundLocalError"
                      f"status = response.status | "
                      f"{e} | "
                      "Уходит в сон")
                continue

        except aiohttp.client_exceptions.ClientHttpProxyError as e:
            print("ClientHttpProxyError")
            try:
                if response.status == 200:
                    tuple_data = (response_text, id_lot, id_auction)
                    data_req.append(tuple_data)
                else:
                    print(f"ClientHttpProxyError | "
                          f"status = {response.status} | "
                          f"{e} | "
                          "Уходит в сон")

                    continue
            except UnboundLocalError as e:
                print(f"ClientHttpProxyError | UnboundLocalError"
                      f"{e} | "
                      "Уходит в сон")
                continue
        except OSError as e:
            print("OSError")
            try:
                if response.status == 200:
                    tuple_data = (response_text, id_lot, id_auction)
                    data_req.append(tuple_data)
                else:
                    print(f"OSError | "
                          f"status = {response.status} | "
                          f"{e} | "
                          "Уходит в сон")
                    continue
            except UnboundLocalError as e:
                print(f"OSError | UnboundLocalError"
                      f"{e} | ")
                continue
            print(f"| OSError |")
            continue
        except UnboundLocalError as e:
            print(e)
        except Exception as e:
            pass
    await add_html_str_pg_asyncpg(data=data_req, type_work=type_work)
    print(f"Запись прошла успешна {id_auction}: [{left_slice} -- {right_slice}]")


async def gather_data(count_create_task, list_id_auction, type_work):
    tasks = []
    logging.warning(
        f"\n*************************\nБудут c работать воркерами {count_create_task} загружены эти данные{list_id_auction}\n*************************\n")
    # по полученному списку аукционов мы итерируемся
    for id_auction in list_id_auction:
        # получение списка всех лотов, котоорый есть в аукционе, берется из бд, которая есть в проекте
        list_id_lot = await get_lot_id_async(
            id_auction)  # получение всех лотов для аукциона
        # (получение из бд, которая была получена путем обращения к аукционам)
        print(f"Получение списка лота для {id_auction}")
        # делим каждый список лотов на равные части, которые указали изначально как делителем count_create_task
        # для получения списка срезов, которые делят по равным частям
        # для каждого воркера список лотов в аукционе
        list_slice = await get_diff_for_equally_async(id_auction,
                                                      count_create_task)
        for slice_border in list_slice:
            task = asyncio.create_task(
                get_page_data(id_auction, slice_border[0], slice_border[1], list_id_lot, type_work))
            tasks.append(task)

    await asyncio.gather(*tasks)

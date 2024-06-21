import asyncio
import csv
import datetime

import sys
import time
import traceback
from http import HTTPStatus

import aiohttp
import logging

from aiohttp.web_exceptions import HTTPError

from get_info_lot_bids.async_src.as_pg_async_write_html import add_html_str_pg_asyncpg

from get_info_lot_bids.async_src.func import make_url_for_get_data_async, get_lot_id_async, \
    get_diff_for_equally_async, write_in_csv_for_loss_url
# from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction # TODO: раскоммитить
from get_info_lot_bids.async_src.help_for_request.list_proxies import get_proxies
from get_info_lot_bids.async_src.help_for_request.list_user_agent import get_headers
from src.note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


async def get_page_data(id_auction, left_slice, right_slice, list_id_lot):
    list_url_loss = []  # для получения не удачных запросов к этим url(не работает)
    try_connect = True  # флаг ждя записи, если вылезла ошибка(не работает)
    data_req = []
    for id_lot in list_id_lot[left_slice:right_slice]:  # идём по циклу получаем срез списка, указанный ранее
        url = await make_url_for_get_data_async(id_auction, id_lot)  # получаем url
        proxy = await get_proxies()  # получаем случаный прокси-сервер(заранее заготовленный список, можно получать по url случайный ip)
        if try_connect:
            try:
                headers = await get_headers()  # получаем случайный заголовок(возможно избегает блокировку)
                async with aiohttp.ClientSession() as session:
                    response = await session.get(url=url, headers=headers, proxy=proxy)
                    if response.status == 200:
                        response_text = await response.text()  # запрос превращаем текста для дальнейшего парсинга
                        # try_conn_db = await add_html_str_pg_asyncpg(html=response_text, id_lot_hidden=id_lot,
                        #                                             id_auction_hidden=id_auction,
                        #                                             try_connect=try_connect)  # запись в базу данных
                        # try_connect = try_conn_db

                        tuple_data = (response_text, id_lot, id_auction)
                        data_req.append(tuple_data)
                        # if len(data)
                        #     pass
                        # try_conn_db = await add_html_str_pg_asyncpg(html=response_text, id_lot_hidden=id_lot,
                        #                                             id_auction_hidden=id_auction,
                        #                                             try_connect=try_connect)  # запись в базу данных
                        # print("Выполненно")
                        # with open("test_async.csv", "w", newline='') as file:
                        #     csv.writer(file).writerow(data_req)
                        # try_connect = try_conn_db

                        # print(f"Отработан аукцион {id_auction}\n"
                        #       f"Отработан лот {id_lot}\n")
                    else:
                        # date_wrong = datetime.datetime.now()
                        logging.error(f"[date_wrong]"
                                      f"Возбуждено исключение на запрос к сервису"
                                      # f"Ошибка при за запросе. Статус кода: {response.status}"
                                      # f"Текст запроса: {response.text()}"
                                      f"{url}"
                                      f"{proxy}"
                                      f"===============================================")
                        # with open("last_url.txt", 'a') as t:
                        #     t.write(f"{url}\n")
                        # raise HTTPError()
            except aiohttp.client_exceptions.ClientProxyConnectionError as e:  # отлов ошибки (интересная штука, что-то возбуждает исключение, что прокси в запросе не работает, но по факту работает и запрос проходит успешно. Также запрашиваемые данные успешно отсылаются) Поэтому, я после этой ошибки записываю данные в бд
                # print("ClientProxyConnectionError")

                # date_wrong = datetime.datetime.now()
                # logging.error(f"==============================================="
                #               f"\n[{date_wrong}]\n"
                #               f"Проблема с прокси {e}\n"
                #               f"{response.status}\n"
                #               # f"{response_text}\n"
                #               f"url запроса <{url}>\n"
                #               f"proxy <{proxy}>\n"
                #               # f"{traceback.format_exc()}\n"
                #               f"===============================================")
                # push_note_mail(email_text=f"Упала ошибка. Проблема в получении данных {e}",
                #                subject_email="Проблема с прокси. Парсер приостановлен на 60 сек")
                # with open("last_url.txt", 'a') as t:
                #     t.write(f"{url}\n")
                # with open("problem_proxy.txt", 'a') as t:
                # t.write(f"{proxy}\n")
                # time.sleep(60)
                # try_connect += 1
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
                        # try_connect = False
                        # заглушка для искусственного торможения итерации, чтобы в случаи ошибки. Скрипт не молотил в холостую
                        # time.sleep(0.1)
                        continue
                except UnboundLocalError as e:
                    print(f"ClientProxyConnectionError | UnboundLocalError"
                          f"status = response.status | "
                          f"{e} | "
                          "Уходит в сон")
                    continue

                    # try_conn_db = await add_html_str_pg_asyncpg(html=response_text, id_lot_hidden=id_lot,
                    #                                             id_auction_hidden=id_auction, try_connect=try_connect)
                    # try_connect = try_conn_db

                    # tuple_data = (response_text, id_lot, id_auction)
                    # data_req.append(tuple_data)
                # else:
                #     print(f"ClientProxyConnectionError | "
                #           f"status = {response.status} | "
                #           f"{e} | "
                #           "Уходит в сон")
                #     try_connect = False
                #     # заглушка для искусственного торможения итерации, чтобы в случаи ошибки. Скрипт не молотил в холостую
                #     time.sleep(20)
            except aiohttp.client_exceptions.ClientHttpProxyError as e:
                print("ClientHttpProxyError")

                # if response.status == 200:
                # try_conn_db = await add_html_str_pg_asyncpg(html=response_text, id_lot_hidden=id_lot,
                #                                             id_auction_hidden=id_auction, try_connect=try_connect)
                # try_connect = try_conn_db
                try:
                    if response.status == 200:
                        tuple_data = (response_text, id_lot, id_auction)
                        data_req.append(tuple_data)
                    else:
                        print(f"ClientHttpProxyError | "
                              f"status = {response.status} | "
                              f"{e} | "
                              "Уходит в сон")
                        # try_connect = False
                        # заглушка для искусственного торможения итерации, чтобы в случаи ошибки. Скрипт не молотил в холостую
                        # time.sleep(0.1)
                        continue
                except UnboundLocalError as e:
                    print(f"ClientHttpProxyError | UnboundLocalError"
                          f"status = response.status | "
                          f"{e} | "
                          "Уходит в сон")
                    continue
                # tuple_data = (response_text, id_lot, id_auction)
                # data_req.append(tuple_data)
                # else:
                # print(f"ClientHttpProxyError | "
                # f"status = {response.status} | "
                # f"{e} | "
                # "Уходит в сон")
                # try_connect = False
                # заглушка для искусственного торможения итерации, чтобы в случаи ошибки. Скрипт не молотил в холостую
                # time.sleep(20)
            except OSError as e:
                print("OSError")
                # date_wrong = datetime.datetime.now()
                # logging.error(f"====="
                #               f"OSError ")
                # f"| [{date_wrong}] "
                # f"| Проблема в получении запроса {e}\n"
                # f"| url запроса <{url}>\n"
                # f"| response.status = {response.status} "
                # f"| proxy <{proxy}>"
                # f"=====")
                # push_note_mail(email_text=f"Упала ошибка. Проблема в получении данных {e}",
                #                subject_email="Проблема с запросом. Парсер перестал работать")
                # print(f"response.status = {response.status}\n"
                #       "Уходит в сон")
                # try_connect = False
                # print(f'try_connect = {try_connect}')
                # print(f"{response.status}"
                #       "Уходит в сон")
                # time.sleep(120)
                # if response.status == 200:
                # try_conn_db = await add_html_str_pg_asyncpg(html=response_text, id_lot_hidden=id_lot,
                #                                             id_auction_hidden=id_auction, try_connect=try_connect)
                # try_connect = try_conn_db
                try:
                    if response.status == 200:
                        tuple_data = (response_text, id_lot, id_auction)
                        data_req.append(tuple_data)
                    else:
                        print(f"OSError | "
                              f"status = {response.status} | "
                              f"{e} | "
                              "Уходит в сон")
                        # try_connect = False
                        # заглушка для искусственного торможения итерации, чтобы в случаи ошибки. Скрипт не молотил в холостую
                        # time.sleep(0.1)
                        continue
                except UnboundLocalError as e:
                    print(f"OSError | UnboundLocalError"
                          f"status = response.status | "
                          f"{e} | "
                          "Уходит в сон")
                    continue
                # tuple_data = (response_text, id_lot, id_auction)
                # data_req.append(tuple_data)
                # else:
                print(f"| OSError | {response.status}"
                      "Уходит в сон. ")
                # try_connect = False
                # time.sleep(20)
                continue
            except UnboundLocalError as e:
                print(e)
            except Exception as e:
                # date_wrong = datetime.datetime.now()
                # logging.error(f"====="
                #               f"Exception "
                #               f"| [{date_wrong}] "
                #               f"| Проблема в получении запроса {e}\n"
                #               f"url запроса <{url}>\n"
                #               f"| response.status = {response.status} "
                #               f"| proxy <{proxy}>"
                #               # f"{traceback.format_exc()}"
                #               f"=====")
                # push_note_mail(email_text=f"Упала ошибка. Проблема в получении данных {e}",
                #                subject_email="Проблема с запросом. Парсер перестал работать")
                # with open("last_url.txt", 'a') as t:
                #     t.write(f"{url}\n")
                # with open("problem_proxy.txt", 'a') as t:
                #     t.write(f"{proxy}\n")
                # print(f"{response.status}"
                #       "Уходит в сон")
                # try_connect = False
                print(f'try_connect = {try_connect}')
                # time.sleep(20)
        else:
            list_url_loss.append(url)  # продолжение итерации для получение не записанный url адресов в бд

    # print(data_req)
    # with open("test_async.csv", "w", newline='') as file:
    #     csv.writer(file).writerow(data_req)
    await add_html_str_pg_asyncpg(data=data_req, try_connect=True)
    print(f"Запись прошла успешна {id_auction}: [{left_slice} -- {right_slice}]")
    # if try_connect is False:
    #     print("Запись не полученных данных")
    #     write_in_csv_for_loss_url(list_url=list_url_loss)


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
    # по полученному списку аукционов мы итереруемся
    for id_auction in list_id_auction:
        # получение списка всех лотов, котоорый есть в аукционе, берется из бд, которая есть в проекте
        list_id_lot = await get_lot_id_async(
            id_auction)  # получение всех лотов для аукциона (получение из бд, которая была получена путем обращения к аукционам)
        print(f"Получение списка лота для {id_auction}")
        # делим каждый список лотов на равные части, которые указали изначально как делителем count_create_task
        list_slice = await get_diff_for_equally_async(id_auction,
                                                      count_create_task)  # для получения списка срезов, которые делят по равным частям для каждого воркера список лотов в аукционе
        for slice_border in list_slice:
            task = asyncio.create_task(
                get_page_data(id_auction, slice_border[0], slice_border[1], list_id_lot))
            tasks.append(task)

    await asyncio.gather(*tasks)

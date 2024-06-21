import asyncio
import csv
import datetime
import logging
import sys
import time
import traceback

from bs4 import BeautifulSoup

from database.db import SessionLocal
from database.db_for_loss_data import SessionLocalLoss, LotAuctionLoss
from database.models import LotAuction
# from get_info_lot_bids.async_src.help_for_request.dict_data_auction_lot import dict_auction_lot # TODO:раскоммитить
from get_info_lot_bids.async_src.help_for_request.dict_data_auction_lot import dict_auction_lot_loss
# from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction # T# TODO:раскоммитить
from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction_loss
from get_info_lot_bids.async_src.help_for_request.list_proxies import get_proxies
from src.note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


async def get_clear_data_async(data):
    # def get_clear_data_async(data):
    """
    Получение отфильтрованных данных. В данный момент не используется из-за изкой скорости
    :param data: полученная страница из запроса
    :return: {'amount_bid': int, 'nickname': str, 'datetime_pay': str, 'status': str}
    """
    # TODO: надо сделать проверку на входные данные
    try:
        soup = BeautifulSoup(data, 'lxml')
        table = soup.find('table')
        results = []
        status_choise = {'first': 'first', 'inter': 'inter', 'final': 'final'}
        count_number_buyer = 0
        rows = table.find_all('tr')[1:]
        all_records_in_list = len(rows)
        for row in rows:
            aux = row.findAll('td')
            bid_to_space: str = aux[0].string
            bid = "".join(bid_to_space.split(' '))
            nickname = aux[2].string
            datetime_pay = aux[3].string
            res = {'amount_bid': bid, 'nickname': nickname, 'datetime_pay': datetime_pay}
            if (all_records_in_list - count_number_buyer) == all_records_in_list:
                res['status'] = status_choise['final']
            elif (all_records_in_list - 1) == count_number_buyer:
                res['status'] = status_choise['first']
            else:
                res['status'] = status_choise['inter']

            try:
                uniq_str = (nickname + "_" + str(bid) +
                            "_" + datetime_pay + "_" + str(count_number_buyer))
                res['uniq_str'] = uniq_str
            except Exception:
                pass
            try:
                uniq_str = (str(bid) +
                            "_" + datetime_pay + "_" + str(count_number_buyer))
                res['uniq_str'] = uniq_str
            except Exception:
                pass
            try:
                uniq_str = (nickname + "_" +
                            "_" + datetime_pay + "_" + str(count_number_buyer))
                res['uniq_str'] = uniq_str
            except Exception:
                pass
            # res['uniq_str'] = uniq_str
            results.append(res)
            count_number_buyer += 1
        return results
        # return "Прочитана запись"
    except AttributeError as e:
        date_wrong = datetime.datetime.now()
        logging.error(f"{date_wrong}"
                      f"{traceback.format_exc()}"
                      f"{e}"
                      f"===============================================")
        push_note_mail(email_text=f"Упала ошибка. Проблема в получении данных: {e}",
                       subject_email="Проблема с таблицей платежей лотов")


async def make_url_for_get_data_async(id_auction_hidden, id_lot_hidden):
    """
    Функция для получения корректного url адреса для получения страницы со ставками
    :param id_auction_hidden: id аукциона в url
    :param id_lot_hidden: id лота в url
    :return: https://www.wolmar.ru/ajax/bids.php?auction_id=1999&lot_id=999999999&time=1234567890
    """
    time_unix = int(time.time())
    pattern = "https://www.wolmar.ru/ajax/bids.php?auction_id=%s&lot_id=%s&time=%s" % (
        id_auction_hidden, id_lot_hidden, time_unix)
    return pattern


# TODO: раскмомитить
async def get_lot_id_async(id_auction_hidden):
# def get_lot_id_async(id_auction_hidden):
    """
    Получение списка лотов по id аукциона
    :param id_auction_hidden: 1987
    :return: [6611341, 6611342, 6611343, 6611344]
    """
    # TODO: исправить для нормальной работы
    # with SessionLocal() as session:
    #     r = [x.id_lot_hidden for x in session.query(LotAuction.id_auction_hidden,
    #                                                 LotAuction.id_lot_hidden, ).filter(
    #         LotAuction.id_auction_hidden == id_auction_hidden).distinct()]
    #     list_id_hidden_lot = r

    with SessionLocalLoss() as session:
        r = [x.id_lot_hidden for x in session.query(LotAuctionLoss.id_auction_hidden,
                                                    LotAuctionLoss.id_lot_hidden, ).filter(
            LotAuctionLoss.id_auction_hidden == id_auction_hidden).distinct()]
        list_id_hidden_lot = r
    return list_id_hidden_lot
# print(get_lot_id_async(198))

def get_auction_id_not_async() -> list:
    """
    Получение списка всех id аукциона
    :return: [31, 32, 33, 34, 35]
    """
    # Todo: для восстановления нормальной работы раскоммистить
    # with SessionLocal() as session:
    #     r = [x.id_auction_hidden for x in session.query(LotAuction.id_auction_hidden).distinct()]
    #     list_id_hidden_auction = r
    # return list_id_hidden_auction

    with SessionLocalLoss() as session:
        r = [x.id_auction_hidden for x in session.query(LotAuctionLoss.id_auction_hidden).distinct()]
        list_id_hidden_auction = r
    return list_id_hidden_auction




def create_dict_record_in_auction(list_id_auctions):
    """
    Создание словаря записией
    :param list_id_auctions:
    :return: {1: 6000, 2: 6000, 3: 6000, }
    """
    dict_record_in_auction = {}
    for id_auction in list_id_auctions:
        count_lots = len(get_lot_id_async(id_auction))
        dict_record_in_auction[id_auction] = count_lots
    return dict_record_in_auction


def get_slice_auction_for_request(all_id_auction, count_rec_in_list):
    list_need_id_auction = all_id_auction[:count_rec_in_list]
    dict_for_create_task_async = create_dict_record_in_auction(list_need_id_auction)
    return dict_for_create_task_async


async def get_diff_for_equally_async(id_auction, count_diff) -> list:
    """
    Служит для получения пар срезов для разрезания списка id lot для распределения на равные части и передачи их в цикл событий асинхронной функции запросов
    :param id_auction: индефикатора в url аукциона
    :param count_diff: количество делений задач на равные части для делегирования асинхронности
    :return: [(None, 31), (31, 62), (62, None)]
    """
    print("\nПолучение срезов для списков\n")
    list_slice_lots = []
    records = dict_auction_lot_loss[id_auction]
    if records < count_diff:
        count_diff = records
    simple_diff = records / count_diff
    if (int(simple_diff) * count_diff) > records:
        simple_diff = int(simple_diff - 1)
    left_border = None
    right_border = simple_diff
    slice_both = (left_border, int(right_border))
    list_slice_lots.append(slice_both)
    for value_slice in range(count_diff)[1:]:
        if left_border is None:
            left_border = value_slice * simple_diff
        else:
            left_border = left_border + simple_diff
        if (value_slice + 1) == count_diff:
            right_border = None
        else:
            right_border = int(right_border + simple_diff)
        slice_both = (int(left_border), right_border)
        list_slice_lots.append(slice_both)
    return list_slice_lots


# использовалось для поулчения словаря dict_data_auction_lot.py
# all = sorted(get_auction_id_not_async(), reverse=True)
# print(all)
# print(get_slice_auction_for_request(all, 1626))
# proxy = get_proxies()
# proxy_ip_def = proxy.split(':')[0]
# proxy_port_def = proxy.split(':')[1]
# print(proxy)
# def change_txt_ip():
#     start = time.time()
#     list_ip = []
#     proxy = get_proxies()
#     for pr in proxy:
#         proxy_ip_def = pr.split(':')[0]
#         proxy_port_def = pr.split(':')[1]
#         prox = f"http://{proxy_ip_def}:{proxy_port_def}"
#         list_ip.append(prox)
#     final = time.time()
#     print(final - start)
#     return list_ip
# print(change_txt_ip())
# TODO: Эта функция не работает
def write_in_csv_for_loss_url(list_url):
    """
    Запись url после отлова ошибки при парсинге
    Если произошла ошибка, то подключение не возможно восстановить
    ТО есть продолжается цикл получения url и этот url записывается в csv
    :param url:
    :return:
    """
    with open('loss_url.csv', 'a', newline='') as filename:
        write_filename = csv.writer(filename, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for url in list_url:
            write_filename.writerow([url])

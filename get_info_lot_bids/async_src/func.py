import asyncio
import datetime
import logging
import sys
import time
import traceback

from bs4 import BeautifulSoup

from database.db import SessionLocal
from database.models import LotAuction
from src.note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


async def get_clear_data_async(data):
# def get_clear_data_async(data):
    """
    Получение отфильтрованных данных
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
                      f"{e}")
        push_note_mail(email_text=f"Упала ошибка. Проблема в получении данных: {e}",
                       subject_email="Проблема с таблицей платежей лотов")


async def make_url_for_get_data_async(id_auction_hidden, id_lot_hidden):
    time_unix = int(time.time())
    pattern = "https://www.wolmar.ru/ajax/bids.php?auction_id=%s&lot_id=%s&time=%s" % (
        id_auction_hidden, id_lot_hidden, time_unix)
    return pattern


async def get_lot_id_async(id_auction_hidden):
    """
    Получение списка лотов по id аукциона
    :param id_auction_hidden: 1987
    :return: [6611341, 6611342, 6611343, 6611344]
    """
    # print("Предположительное место падения")
    with SessionLocal() as session:
        r = [x.id_lot_hidden for x in session.query(LotAuction.id_auction_hidden,
                                                    LotAuction.id_lot_hidden, ).filter(
            LotAuction.id_auction_hidden == id_auction_hidden).distinct()]
        list_id_hidden_lot = r

    return list_id_hidden_lot
    # return [1217, 1218, 1223, 1222]


def get_auction_id_not_async():
    """
    Получение списка всех id аукциона
    :return: [31, 32, 33, 34, 35]
    """

    with SessionLocal() as session:
        r = [x.id_auction_hidden for x in session.query(LotAuction.id_auction_hidden).distinct()]
        list_id_hidden_auction = r
    return list_id_hidden_auction

import logging
import time

from get_info_auction_and_lot.src_auction.db import SessionLocal
from get_info_auction_and_lot.src_auction.models import LotAuction

from get_info_lot_and_bids.help_for_request_bids.dict_data_auction_lot import dict_auction_lot

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


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
    """
    Получение списка лотов по id аукциона
    :param id_auction_hidden: 1987
    :return: [6611341, 6611342, 6611343, 6611344]
    """
    # TODO: исправить для нормальной работы
    with SessionLocal() as session:
        r = [x.id_lot_hidden for x in session.query(LotAuction.id_auction_hidden,
                                                    LotAuction.id_lot_hidden, ).filter(
            LotAuction.id_auction_hidden == id_auction_hidden).distinct()]
        list_id_hidden_lot = r

    return list_id_hidden_lot


async def get_diff_for_equally_async(id_auction, count_diff) -> list:
    """
    Служит для получения пар срезов для разрезания списка id lot для распределения на равные части и передачи их в цикл событий асинхронной функции запросов
    :param id_auction: индефикатора в url аукциона
    :param count_diff: количество делений задач на равные части для делегирования асинхронности
    :return: [(None, 31), (31, 62), (62, None)]
    """
    print("\nПолучение срезов для списков\n")
    list_slice_lots = []
    records = dict_auction_lot[id_auction]
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

import sys
from os.path import dirname, abspath
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from get_info_auction_and_lot.src_auction.db import SessionLocal
from get_info_auction_and_lot.src_auction.models import LotAuction


def get_auction_id_not_async() -> list:
    """
    Получение списка всех id аукциона
    :return: [31, 32, 33, 34, 35]
    """
    with SessionLocal() as session:
        r = [x.id_auction_hidden for x in session.query(LotAuction.id_auction_hidden).distinct()]
        list_id_hidden_auction = r
    return list_id_hidden_auction


def get_lot_id_async(id_auction_hidden):
    """
    Получение списка лотов по id аукциона
    :param id_auction_hidden: 1987
    :return: [6611341, 6611342, 6611343, 6611344]
    """
    with SessionLocal() as session:
        r = [x.id_lot_hidden for x in session.query(LotAuction.id_auction_hidden,
                                                    LotAuction.id_lot_hidden, ).filter(
            LotAuction.id_auction_hidden == id_auction_hidden).distinct()]
        list_id_hidden_lot = r

    return list_id_hidden_lot


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


def get_slice_auction_for_request(all_id_auction: list, count_rec_in_list: int) -> dict:
    list_need_id_auction = all_id_auction[:count_rec_in_list]
    dict_for_create_task_async = create_dict_record_in_auction(list_need_id_auction)
    return dict_for_create_task_async


def main():
    """
    Тут же можно получить список id action,  который есть уже в бд в storage_coin.db

    Нужна для пулчения словаря. Сохранить и засунуть в файл
    get_info_lot_and_bids/help_for_request_bids/dict_data_auction_lot.py
    Просто сохранить dict_auction_lot и назвать словарь этим именем
    :return:
    """
    list_all_auction = sorted(get_auction_id_not_async(), reverse=True)
    print(f"{list_all_auction}\n")
    # print(create_dict_record_in_auction(get_lot_id_async(1990)))
    print(get_slice_auction_for_request(list_all_auction, len(list_all_auction)))


if __name__ == "__main__":
    main()

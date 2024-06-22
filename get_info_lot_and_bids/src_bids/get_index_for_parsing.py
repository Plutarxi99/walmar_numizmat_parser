import logging

from get_info_auction_and_lot.src_auction.parser_data import get_all_number_auction
from get_info_lot_and_bids.help_for_request_bids.list_id_auction import list_id_hidden_auction

"""
Поулчение инжекса с которого можно начать парсинг
И получение списка для визуального осмотра можно сохранить
"""


def get_index_in_list(id_auction):
    # list_id_auction = get_all_number_auction()
    list_id_auction = list_id_hidden_auction[:]
    reverse_list = sorted(list_id_auction, reverse=True)
    return reverse_list, reverse_list.index(id_auction)


if __name__ == "__main__":
    id_auction = 1990
    list_id, index_auc = get_index_in_list(id_auction)
    print("Твой индекс, который ты ищешь", index_auc)
    print("Список от 0 до 10 после указанного индекса\n", sorted(list_id, reverse=True)[index_auc:10+index_auc])

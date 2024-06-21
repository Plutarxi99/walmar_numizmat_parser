import logging

from get_info_auction_and_lot.src_auction.parser_data import get_all_number_auction

"""
Поулчение инжекса с которого можно начать парсинг
И получение списка для визуального осмотра можно сохранить
"""


def get_index_in_list(id_auction):
    list_id_auction = get_all_number_auction()
    return list_id_auction, list_id_auction.index(id_auction)


if __name__ == "__main__":
    id_auction = 1989
    list_id, index_auc = get_index_in_list(id_auction)
    print("Твой индекс, который ты ищешь", index_auc)
    print("Список от 0 до 50\n", sorted(list_id, reverse=True)[0:50])

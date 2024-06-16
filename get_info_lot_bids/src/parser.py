import datetime

from bs4 import BeautifulSoup

from database.db import SessionLocal
from database.models import LotAuction
from get_info_lot_bids.src.get import get_data_bids_pass_test, get_data_bids


# TODO: 0:00:00.266212 обработка одного запроса для получение всех ставок
# TODO: 23 минуты только для получение списка url
def get_soup(data):
    soup = BeautifulSoup(data, 'lxml')
    return soup


def get_auction_id():
    """
    Получение списка всех id аукциона
    :return: [31, 32, 33, 34, 35]
    """

    with SessionLocal() as session:
        r = [x.id_auction_hidden for x in session.query(LotAuction.id_auction_hidden).distinct()]
        list_id_hidden_auction = r
    return list_id_hidden_auction


def get_lot_id(id_auction_hidden):
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


def make_url_for_get_data(id_auction_hidden, id_lot_hidden):
    pattern = "https://www.wolmar.ru/ajax/bids.php?auction_id=%s&lot_id=%s" % (id_auction_hidden, id_lot_hidden)
    return pattern


def get_list_url_for_parser(id_auction_hidden):
    """
    Для получения готового списка url на который будет сделан запрос
    :param id_auction_hidden: id аукциона указанный в url
    :return: ['https://www.wolmar.ru/ajax/bids.php?auction_id=1960&lot_id=6611341', ....]
    """
    list_url = []
    list_id_lot = get_lot_id(id_auction_hidden=id_auction_hidden)
    for id_lot in list_id_lot:
        url_for_parser = make_url_for_get_data(id_auction_hidden=id_auction_hidden,
                                               id_lot_hidden=id_lot)
        list_url.append(url_for_parser)
    print(len(list_url))
    return list_url


def get_clear_data(soup):
    """
    Получение отфильтрованных данных
    :param soup:
    :return:
    """
    # TODO: надо сделать проверку на входные данные
    try:
        table = soup.find('table')
        results = []
        status_choise = {'first': 'first', 'inter': 'inter', 'final': 'final'}
        count_number_buyer = 0
        rows = table.find_all('tr')[1:]
        all_records_in_list = len(rows)
        # print(all_records_in_list)
        for row in rows:
            aux = row.findAll('td')
            bid_to_space: str = aux[0].string
            amount_bid = "".join(bid_to_space.split(' '))
            res = {'amount_bid': amount_bid, 'nickname': aux[2].string, 'datetime_pay': aux[3].string}
            if (all_records_in_list - count_number_buyer) == all_records_in_list:
                res['status'] = status_choise['final']
            elif (all_records_in_list - 1) == count_number_buyer:
                res['status'] = status_choise['first']
            else:
                res['status'] = status_choise['inter']
            uniq_str = (aux[2].string + "_" + str(amount_bid) +
                        "_" + aux[3].string + "_" + str(count_number_buyer))
            res['uniq_str'] = uniq_str
            results.append(res)
            count_number_buyer += 1

        return results
    except AttributeError as e:
        print("Получение страницы без данных")


start = datetime.datetime.now()
print(start)
# data = get_data_bids_pass_test(url='../data/lot1.html')
# https://www.wolmar.ru/auction/913/1330670
# https://www.wolmar.ru/auction/34/1966
# https://www.wolmar.ru/auction/35/2055
# https://www.wolmar.ru/auction/67/12528
# https://www.wolmar.ru/auction/76/18027
# data = get_data_bids(url='https://www.wolmar.ru/ajax/bids.php?auction_id=35&lot_id=2055')
data = get_data_bids(url='https://www.wolmar.ru/ajax/bids.php?auction_id=76&lot_id=18027')
# data = get_data_bids_pass_test()
soup = get_soup(data)
clear_data = get_clear_data(soup)
print(clear_data)
if clear_data is None or clear_data == []:
    print("ОТработала")
# print(data)
# print(get_lot_id(1960))
# print(get_auction_id())
# get_auction_id()
# lot = get_lot_id(1960)[5]
# print(make_url_for_get_data(1960, lot))
# print(get_list_url_for_parser(1960))
end = datetime.datetime.now()
print(end - start)

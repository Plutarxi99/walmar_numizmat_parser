import traceback
from datetime import datetime
import re
import bs4.element

from config import settings
from get_info_auction_and_lot.src_auction.get_data import get_data_from_page
from bs4 import BeautifulSoup

from get_info_auction_and_lot.src_auction.work_with_last_iter import get_path_to_file_log


def get_soup_parser(data: str):
    """
    Полученние экземпляра BeautifulSoup для передачи в функции
    :param data: текстовый файл html кода страницы полученный из запроса
    :return: объект BeautifulSoup
    """
    try:
        soup = BeautifulSoup(data, "lxml")  # с этой настройкой работает лучше
        return soup
    except TypeError as e:
        print(f"Ошибка произошла в модуле 'src.parser_data.get_soup_parser'"
              f"Получен ответ от запроса 'None', проверь запрос:\n"
              f"Оригинальный текст ошибки:\n{e}")


def get_all_number_auction():
    """
    Получение всех id аукционов содержащихся на главной странице
    "data_test/main_page_site.html"
    :return: ['1983', '1980', '1978', '1976',...]
    """
    data = get_data_from_page(url=settings.URL_DOMEN)
    soup = get_soup_parser(data)
    list_auction = []
    vip_first_url = soup.find('a', attrs={"class": "current current_dark"})
    vip_first = vip_first_url.attrs['href'].split('/')[2]
    list_auction.append(vip_first)
    vip_url = soup.find('div', attrs={"class": "right_box_dark"})
    vip_href = vip_url.select("a")
    for vip in vip_href:
        value_vip = vip.attrs['href'].split('/')[2]
        list_auction.append(value_vip)
    std_first_url = vip_url.find_next('a', attrs={"class": "current"})
    std_first = std_first_url.attrs['href'].split('/')[2]
    list_auction.append(std_first)
    std_url = soup.find('div', attrs={"class": "right_box"})
    std_href = std_url.select("a")
    for std in std_href:
        value_std = std.attrs['href'].split('/')[2]
        list_auction.append(value_std)
    rev_list_auction = list(map(int, list_auction))
    res = sorted(rev_list_auction)
    return res


def get_dict_number_auction_type():
    """
    Получение всех id аукционов содержащихся на главной странице и их принадлежность к типу аукциона
    "data_test/main_page_site.html"
    :return: {1986: 'std', 1985: 'vip', 1984: 'std', 1983: 'vip', 1982: 'std'...}
    """
    data = get_data_from_page(url=settings.URL_DOMEN)
    soup = get_soup_parser(data)
    dict_auction = {}
    vip_first_url = soup.find('a', attrs={"class": "current current_dark"})
    vip_first = vip_first_url.attrs['href'].split('/')[2]
    dict_auction[int(vip_first)] = 'vip'
    vip_url = soup.find('div', attrs={"class": "right_box_dark"})
    vip_href = vip_url.select("a")
    for vip in vip_href:
        value_vip = vip.attrs['href'].split('/')[2]
        dict_auction[int(value_vip)] = 'vip'

    std_first_url = vip_url.find_next('a', attrs={"class": "current"})
    std_first = std_first_url.attrs['href'].split('/')[2]
    dict_auction[int(std_first)] = 'std'
    std_url = soup.find('div', attrs={"class": "right_box"})
    std_href = std_url.select("a")
    for std in std_href:
        value_std = std.attrs['href'].split('/')[2]
        dict_auction[int(value_std)] = 'std'
    res = dict(sorted(dict_auction.items(), reverse=True))
    return res


def parser_info_auction(soup):
    """
    Получение информации о аукционе
    :param soup:
    :return: {'title_auction': str, 'date_closed': str, 'id_auction_visible': int}
    """

    info_auction = {}
    try:
        get_info_auction = soup.find('h1').text.split()  # TODO: спорное решение возможно получение ошибок
        # если акцион в данный момент работает, то у него нет даты закрытия
        try:
            title_auction = " ".join(get_info_auction[2:5])  # получение название аукциона
            pattern = r"аукцион №\d+"
            string = title_auction
            if re.match(pattern, string):
                title_auction = re.search(pattern, string).group()
        except IndexError as e:
            print(f"Аукцион имеет не стандартный заголовок.\n"
                  f"Получено: {get_info_auction}\n"
                  f"Проблема в поле title_auction\n"
                  f"Оригинальный текст ошибки: {e}\n")
            title_auction = " ".join(get_info_auction[2:])
        try:
            date_closed = get_info_auction[6] + ' ' + get_info_auction[7][:-1]  # дата закрытия аукциона

        except IndexError as e:
            print(f"Аукцион не имеет даты окончания. Он не закончился.\n"
                  f"Получено: {get_info_auction}\n"
                  f"Ошибка отловлена. Все хорошо")
            # для новых аукционов нет даты, поэтому ставлю прочерк
            try:
                date_closed = get_info_auction[5] + ' ' + get_info_auction[6][:-1]
            except:
                date_closed = ''
        try:
            info_auction['title_auction'] = title_auction
            info_auction['date_closed'] = date_closed
            pattern = r"\d+"
            info_auction['id_auction_visible'] = re.search(pattern, title_auction).group()
        except AttributeError as e:
            print("Стоит пробел между <№> and <79>, устраняю проблему")
            title_auction = " ".join(get_info_auction[2:5]) + "".join(get_info_auction[5])
            date_closed = get_info_auction[7] + ' ' + get_info_auction[8][:-1]
            info_auction['title_auction'] = title_auction
            try:
                info_auction['date_closed'] = date_closed
            except Exception:
                info_auction['date_closed'] = ''
            pattern = r"\d+"
            info_auction['id_auction_visible'] = re.search(pattern, title_auction).group()
        return info_auction
    except Exception as e:
        print(f"Ошибка произошла в модуле 'src.parser_data.parser_info_auction'"
              f"Оригинальный текст ошибки:\n{e}"
              f"{traceback.format_exc()}")


def parser_table_info(soup, date_closed, id_auction_visible, type_auction):
    """
    Получение информации из истории лотов из таблицы
    :param soup: экземпляр класса BeautifulSoup
    :param id_auction_visible:
    :param date_closed: дата закрытия торгов на аукционе
    :param type_auction:
    :return: [{'title_lot': str, 'year_coin': int, 'mint': str,
    'metal_gr': str, 'safety': str,'buyer': str, 'bids': int,
     'amount': int, 'status': str, 'full_url': str,
     'id_auction_hidden': int, 'id_auction_visible': int,
     'id_lot_hidden': int}, {}]
    """
    print("Парсим страницу")
    storage_auction = []
    table = soup.find('table', attrs={'class': 'colored'})
    # мы берем нужную таблицу отрезав от нее первые теги с помощью среза
    for row in table.find_all('tr')[3:]:  # TODO: спорное решение ???? надо по-другому

        columns: bs4.element.ResultSet = row.find_all(['td', 'th'])
        # В таблице могут быть снятые с лота вещи и поэтому,
        # мы отлавливаем ошибку обращение к несуществущему индексу списка
        try:
            title_lot = columns[1].text.strip()  # название монеты "Название"
            year_coin = columns[2].text.strip()  # год выпуска монеты "Год"
            mint = columns[3].text.strip()  # монетный двор "Буквы"
            metal_gr = columns[4].text.strip()  # "Металл, гр"
            safety = columns[5].text.strip()  # "Сохранность"
            buyer = columns[6].text.strip()  # "Лидер"
            bids = columns[7].text.strip()  # "Ставок"
            amount_str = columns[8].text.strip()
            amount = amount_str if amount_str == '' else ''.join(amount_str.split(' '))  # "Сумма, руб"
            status = columns[9].text.strip()  # "Закрытие"
            href = row.find('a', attrs={'class': 'title lot'})
            url_part_coin = href.attrs['href']
            full_url = settings.URL_DOMEN + url_part_coin  # url на одну штуку лота
            attrs_url = url_part_coin.split('/')
            id_lot_hidden = ''.join(attrs_url[-1:])
            id_auction_hidden = ''.join(attrs_url[-2:-1])

            row = {'title_lot': title_lot,
                   'year_coin': year_coin, 'mint': mint,
                   'metal_gr': metal_gr, 'safety': safety,
                   'buyer': buyer, 'bids': bids,
                   'amount': amount, 'status': status,
                   'full_url': full_url, 'id_auction_hidden': id_auction_hidden,
                   'id_lot_hidden': id_lot_hidden, 'id_auction_visible': id_auction_visible,
                   'date_closed': date_closed, 'type_auction': type_auction
                   }
            storage_auction.append(row)
        except IndexError:
            continue
        except ValueError as e:
            now = datetime.now()
            print(f"Ошибка обработана и записана в логи время: {now}")
            tr_b = traceback.format_exc()
            info_log = f'[{now}] -- [не смог обработать данные] [{tr_b}] -- [{e}]\n'
            path_to_file_log = get_path_to_file_log()
            with open(path_to_file_log, 'a') as txt:
                txt.write(info_log)
    return storage_auction
# with open("./res_test.txt", 'r') as t:
#
#     soup = get_soup_parser(t)
#     print(parser_table_info(soup, 1, 1, 'std'))
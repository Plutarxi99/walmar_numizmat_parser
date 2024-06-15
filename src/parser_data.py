import traceback
from datetime import datetime
from pathlib import Path
import re
import bs4.element

from config import settings
from src.get_data import get_data_from_page_pass_test, get_data_from_page
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent

path = BASE_DIR.__str__() + '/data_test/test_history_auction_all_page.html'
data_test = get_data_from_page_pass_test(url=path)


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
    # path_number = BASE_DIR.__str__() + '/data_test/main_page_site.html'
    # data = get_data_from_page_pass_test(path_number)
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
    # path_number = BASE_DIR.__str__() + '/data_test/main_page_site.html'
    # data = get_data_from_page_pass_test(path_number)
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
                  f"Проблема в поле date_closed\n"
                  f"Оригинальный текст ошибки: {e}")
            # для новых аукционов нет даты, поэтому ставлю прочерк
            try:
                date_closed = get_info_auction[5] + ' ' + get_info_auction[6][:-1]
            except:
                date_closed = ''

        # TODO: нужны ли категории??? Уже готовое решение для получение всех категорй
        # category_auction = []
        # category = soup.find('div', attrs={"class": "submenu"})
        # for cat in category.select("a")[1:]:
        # получение slug из url для дополнительного получение категорий из запроса
        # url_on_category = cat.attrs['href'].split('/', )[3]
        # name_category_on_rus = cat.text  # TODO: ???? нужны ли русские названия категорий ????
        # category_auction.append(url_on_category)
        # info_auction['category_auction'] = category_auction
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


# data = get_data_from_page_pass_test('../data_test/other_change_cod_html_vip.html')
# data = get_data_from_page_pass_test('../data_test/other_change_cod_html_vip_new.html')
# data = get_data_from_page_pass_test('../data_test/test_history_auction_one_page.html')
# data = get_data_from_page_pass_test('../data_test/other_change_cod_html_std.html')
# data = get_data_from_page_pass_test('../data_test/page_error_date_closed.html') # ['расширенный', 'поиск', 'Аукцион', 'Standart', '№', '79', '(Закрыт', '07.09.2011', '11:00)']
# data = get_data_from_page_pass_test('../data_test/page_error_date_closed_454.html') # ['расширенный', 'поиск', 'Аукцион', 'VIP', '№252', '(Закрыт', '01.09.2011', '12:25)']
# data = get_data_from_page_pass_test('../data_test/error_1986.html')
# soup = get_soup_parser(data)
# print(parser_info_auction(soup))


def parser_table_info(soup, date_closed, id_auction_visible, type_auction):
    """
    Получение информации из истории лотов из таблицы
    :param soup: экземпляр класса BeautifulSoup
    :param id_auction_visible:
    :param date_closed: дата закрытия торгов на аукционе
    :param type_auction:
    :return: [('title_lot': str, 'year_coin': int, 'mint': str,
    'metal_gr': str, 'safety': str,'buyer': str, 'bids': int,
     'amount': int, 'status': str, 'full_url': str,
     'id_auction_hidden': int, 'id_auction_visible': int,
     'id_lot_hidden': int), ()]
    """
    # start = datetime.now()
    # print(start)
    print("Парсим страницу")
    storage_auction = []
    table = soup.find('table', attrs={'class': 'colored'})
    # мы берем нужную таблицу отрезав от нее первые теги с помощью среза
    for row in table.find_all('tr')[3:]:  # TODO: спорное решение ???? надо по-другому

        columns: bs4.element.ResultSet = row.find_all(['td', 'th'])
        # В таблице могут быть снятые с лота вещи и поэтому,
        # мы отлавливаем ошибку обращение к несуществущему индексу списка
        try:
            # number_in_site = columns[0].text.strip()  # порядковый номер страницы "ID"
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
            # type_auction =
            id_auction_hidden = ''.join(attrs_url[-2:-1])

            # print(number_in_site, title_lot, year_coin, mint, metal_gr, safety, buyer, bids, amount, status, full_url)
            # row = (number_in_site, title_lot, year_coin, mint, metal_gr, safety, buyer, bids, amount, status, full_url)
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
            with open("data_test/log.txt", 'a') as txt:
                txt.write(info_log)

    # end = datetime.now() - start
    # print(end)  # одна страница -- 0:00:00.050910 # все страницы одного аукциона -- 0:00:04.313387
    return storage_auction

# print(get_all_number_auction())
# print(parser_info_auction(get_soup_parser(data_test)))
# print(parser_table_info(get_soup_parser(data_test), category_auction=''))
# test_data_for_db_one_page = parser_table_info(get_soup_parser(data_test))
# test_data_for_db_all_page = parser_table_info(get_soup_parser(data_test))

import traceback
from datetime import datetime
from pathlib import Path

import bs4.element

from config import settings
from src.get_data import get_data_from_page_pass_test
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
        # soup = BeautifulSoup(data, "html.parser")  # с этим распарсиром работает дольше
        return soup
    except TypeError as e:
        print(f"Ошибка произошла в модуле 'src.parser_data.get_soup_parser'"
              f"Получен ответ от запроса 'None', проверь запрос:\n"
              f"Оригинальный текст ошибки:\n{e}")


def get_all_number_auction_vip():
    """
    Получение всех id аукционов содержащихся на главной странице
    Захардкодено, если трбуется обновление надо скопировать html страницу по пути
    "data_test/main_page_site.html"
    :return: ['1983', '1980', '1978', '1976',...]
    """
    path_number = BASE_DIR.__str__() + '/data_test/main_page_site.html'
    data = get_data_from_page_pass_test(path_number)
    soup = get_soup_parser(data)
    list_vip = []
    # dict_vip = {}
    # list_std = []
    # dict_std = {}
    vip_url = soup.find('div', attrs={"class": "right_box_dark"})
    vip_href = vip_url.select("a")
    for vip in vip_href:
        list_vip.append(vip.attrs['href'].split('/')[2])
        # dict_vip[vip.attrs['href']] = False
    # std_url = soup.find('div', attrs={"class": "right_box"})
    # std_href = std_url.select("a")
    # for std in std_href:
    # dict_std[std.attrs['href']] = False

    return list_vip


def parser_info_auction(soup):
    """
    Получение информации о аукционе
    :param soup:
    :return: {'title_auction': str, 'date_closed': str, 'type': 'std | vip', 'category_auction': list}
    """

    info_auction = {}
    category_auction = []
    try:
        get_info_auction = soup.find('h1').text.split()  # TODO: спорное решение возможно получение ошибок
        # title_auction = get_info_auction[2:5]  # получение название аукциона
        title_auction = " ".join(get_info_auction[2:5])  # получение название аукциона
        date_closed = get_info_auction[6]  # дата закрытия аукциона
        category = soup.find('div', attrs={"class": "submenu"})
        for cat in category.select("a")[1:]:
            # получение slug из url для дополнительного получение категорий из запроса
            url_on_category = cat.attrs['href'].split('/', )[3]
            # name_category_on_rus = cat.text  # TODO: ???? нужны ли русские названия категорий ????
            category_auction.append(url_on_category)

        info_auction['title_auction'] = title_auction
        info_auction['date_closed'] = date_closed
        info_auction['category_auction'] = category_auction
        return info_auction
    except Exception as e:
        print(f"Ошибка произошла в модуле 'src.parser_data.parser_info_auction'"
              f"Оригинальный текст ошибки:\n{e}")


def parser_table_info(soup, category_auction):
    """
    Получение информации из истории лотов из таблицы
    :param soup:
    :param data: строка полученная путем обращения к url
    :return: [(id, Название, Год, Буквы, "Металл, гр", Сохранность, Лидер, Ставок, "Сумма, руб", Закрытие, url, category), ()]
    """
    # start = datetime.now()
    # print(start)
    print("Парсим страницу")
    storage_auction = []
    not_amount = []
    table = soup.find('table', attrs={'class': 'colored'})
    # мы берем нужную таблицу отрезав от нее первые теги с помощью среза
    for row in table.find_all('tr')[3:]:  # TODO: спорное решение ???? надо по-другому

        columns: bs4.element.ResultSet = row.find_all(['td', 'th'])
        # В таблице могут быть снятые с лота вещи и поэтому,
        # мы отлавливаем ошибку обращение к несуществущему индексу списка
        try:
            number_in_site = columns[0].text.strip()  # порядковый номер страницы "ID"
            title_lot = columns[1].text.strip()  # название монеты "Название"
            year_coin = columns[2].text.strip()  # год выпуска монеты "Год"
            mint = columns[3].text.strip()  # монетный двор "Буквы"
            metal_gr = columns[4].text.strip()  # "Металл, гр"
            safety = columns[5].text.strip()  # "Сохранность"
            buyer = columns[6].text.strip()  # "Лидер"
            bids = columns[7].text.strip()  # "Ставок"
            amount_str = columns[8].text.strip()
            if amount_str == '':
                not_amount.append(amount_str)
            # amount = columns[8].text.strip()  # "Сумма, руб"
            amount = amount_str if amount_str == '' else ''.join(amount_str.split(' '))  # "Сумма, руб"
            status = columns[9].text.strip()  # "Закрытие"
            href = row.find('a', attrs={'class': 'title lot'})
            url_part_coin = href.attrs['href']
            full_url = settings.URL_DOMEN + url_part_coin  # url на одну штуку лота
            # print(number_in_site, title_lot, year_coin, mint, metal_gr, safety, buyer, bids, amount, status, full_url)
            # row = (number_in_site, title_lot, year_coin, mint, metal_gr, safety, buyer, bids, amount, status, full_url)
            # row = {'number_in_site': number_in_site, 'title_lot': title_lot,
            #        'year_coin': year_coin, 'mint': mint,
            #        'metal_gr': metal_gr, 'safety': safety,
            #        'buyer': buyer, 'bids': bids,
            #        'amount': amount, 'status': status,
            #        'full_url': full_url}
            row = {'title_lot': title_lot,
                   'year_coin': year_coin, 'mint': mint,
                   'metal_gr': metal_gr, 'safety': safety,
                   'buyer': buyer, 'bids': bids,
                   'amount': amount, 'status': status,
                   'full_url': full_url, 'type_category': category_auction}

            storage_auction.append(row)
        except IndexError as e:
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
    # return not_amount
    return storage_auction


# print(get_all_number_auction())
# print(parser_info_auction(get_soup_parser(data_test)))
# print(parser_table_info(get_soup_parser(data_test), category_auction=''))
# test_data_for_db_one_page = parser_table_info(get_soup_parser(data_test))
# test_data_for_db_all_page = parser_table_info(get_soup_parser(data_test))

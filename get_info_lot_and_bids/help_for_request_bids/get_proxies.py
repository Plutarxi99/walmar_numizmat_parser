import asyncio
import random
import sys

# from get_info_lot_and_bids.help_for_request_bids.list_proxies_static import list_proxies_static


async def get_proxies():
    """
    Функция для поулчения рандомного прокси
    :return: 'http://111.111.111.111:9999'
    """
    try:
        list_proxies_id_port_def = list_proxies_static
        # proxies = f'http://{settings.PROXIES_EMAIL}:{settings.PROXIES_PASS}@{pr}'
        proxy = random.randint(0, len(list_proxies_id_port_def) - 1)
        pr = list_proxies_id_port_def[proxy]
        proxies = f'{pr}'
        return proxies
    except NameError as e:
        print(
            "Загрузи прокси. Как статические в файл .py. "
            "К примеру: get_info_lot_and_bids/help_for_request_bids/list_proxies_static.py\n"
            "Создай файл указанный в пути и вставь туда список id прокси"
            "\nПо типу: ['http://111.111.111.111:9999', 'http://111.111.111.111:9999',]")
        return None
    except Exception as e:
        print(
            "Загрузи прокси. Как статические в файл .py. "
            "К примеру: get_info_lot_and_bids/help_for_request_bids/list_proxies_static.py\n"
            "Создай файл указанный в пути и вставь туда список id прокси"
            "\nПо типу: ['http://111.111.111.111:9999', 'http://111.111.111.111:9999',]")
        return None


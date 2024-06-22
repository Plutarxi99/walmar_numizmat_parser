import asyncio
import random

# from get_info_lot_and_bids.help_for_request_bids.list_user_agent_static import list_user_agent_static


async def get_headers():
    """
    Функция для получения рандомного заголовка
    :return:
    """
    try:
        list_headers = list_user_agent_static[:]
        headers = list_headers[random.randint(0, len(list_headers) - 1)]
    except NameError as e:
        print(
            "!!!!!Программа продолжает работать!!!!\n"
            "Загрузи список user-agent. Как статические в файл .py. "
            "К примеру: get_info_lot_and_bids/help_for_request_bids/list_user_agent_static.py\n"
            "Создай файл указанный в пути и вставь туда список user-agent"
            "\nПо типу:\n"
            '"[{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.750 Yowser/2.5 Safari/537.36"},\n'
            '{"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}]"')
        list_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.750 Yowser/2.5 Safari/537.36"}
        headers = list_headers
    except ModuleNotFoundError as e:
        print(
            "!!!!!Программа продолжает работать!!!!\n"
            "Загрузи список user-agent. Как статические в файл .py. "
            "К примеру: get_info_lot_and_bids/help_for_request_bids/list_user_agent_static.py\n"
            "Создай файл указанный в пути и вставь туда список user-agent"
            "\nПо типу:\n"
            '"[{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.750 Yowser/2.5 Safari/537.36"},\n'
            '{"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}]"')
        list_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.750 Yowser/2.5 Safari/537.36"}
        headers = list_headers
    list_accept = [
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"]
    headers["Accept"] = list_accept[random.randint(0, len(list_accept) - 1)]
    headers["sec-ch-ua"] = '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"'
    headers["X-Requested-With"] = "XMLHttpRequest"
    # headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-User"] = "?1"
    # headers["Sec-Fetch-Site"] = "none"
    # headers["Sec-Fetch-Mode"] = "navigate"
    # headers["Sec-Fetch-Dest"] = "document"
    # headers["Host"] = "www.wolmar.ru"
    # headers["Connection"] = "keep-alive"
    # headers["Cache-Control"] = "max-age=0"
    headers["Accept-Language"] = "ru,en;q=0.9,uk;q=0.8"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    # headers["sec-ch-ua-mobile"] = "?0"
    return headers

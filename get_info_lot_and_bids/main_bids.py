import asyncio
import datetime
import logging
import time
import sys
from os.path import abspath, dirname
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from get_info_lot_and_bids.help_for_request_bids.list_id_auction import list_id_hidden_auction

from note_finally_parser import push_note_mail

from get_info_lot_and_bids.pre_start import get_auction_id_not_async

from get_info_lot_and_bids.src_bids.get import gather_data

from config import settings

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


def main(count_create_task, list_for_request, type_work):
    start_main = datetime.datetime.now()
    start_time = time.time()
    logging.warning(f"====="
                    f"Начало скрипта {start_main}"
                    f"=====\n")
    # создание цикла событий и запуск асинхронной кода
    asyncio.run(gather_data(count_create_task, list_for_request, type_work))
    finish_time = time.time() - start_time
    finish_main = datetime.datetime.now() - start_main
    print(f"Затраченное на работу скрипта время: {finish_time}")
    logging.warning(f"====="
                    f"Затраченное время на скрипт сек: {finish_time}"
                    f"Конец скрипта:{finish_main}"
                    f"=====\n")


def get_slice_id_auction(get_i_want_auction: int, past_i_want_auction: int, list_id_auction: list) -> list:
    """
    Получение разреза списка, который будет загружен
    :param get_i_want_auction: сколько аукционов я хочу получить
    :param past_i_want_auction: от какого аукциона  убдет отсчет
    :param list_id_auction: список всех аукционов
    :return: список аукционов, который будет загружен
    """
    right_border = past_i_want_auction + get_i_want_auction
    slice_for_request = list_id_auction[past_i_want_auction:right_border]
    return slice_for_request


def safety_cancel(sec_sleep, list_id_auc, past_i_want_auc):
    push_note_mail(
        email_text=f"Безопасное отключание парсера в течении секунд {sec_sleep}\n"
                   f"Загружены аукционы {list_id_auc}\n"
                   f"Остановлена на итерации:{past_i_want_auc}",
        subject_email="Внимание, можно отключить безопасно парсер")
    time.sleep(sec_sleep)


if __name__ == "__main__":
    count_create_task = 100
    past_i_want_auction = 2
    get_i_want_auction = 1
    safe_canc = 180
    type_work = settings.TYPE_WORK  # если не указывать будет аснхронная запись в postgresql, иначе оставить просто ковычки
    # можно статически указать файл или брать из таблицы,
    # которая было создана в get_info_auction_and_lot/main_auction.py
    list_id_auction = list_id_hidden_auction[:]
    logging.warning(f"====="
                    f"Создано воркеров {count_create_task} "
                    f"| Установлен индекс {past_i_want_auction} "
                    f"| Загружается аукционов {get_i_want_auction} "
                    f"| Задержка safe cancel {safe_canc}"
                    f"=====\n")
    # длина получаемого списка от указанного последнего индекса из списка id аукционов
    # нужен для того, чтобы вызывать не весь список, а разделить на равные
    # загружаемые части
    count_length = len(list_id_auction) - past_i_want_auction
    print(count_length)
    # количество итераций запускаемым скриптом
    count_iter = int(count_length / get_i_want_auction)
    for x in range(count_iter):
        # получаем список, который будет загружен
        list_for_request = get_slice_id_auction(get_i_want_auction, past_i_want_auction, list_id_auction)
        # последняя итерация, которая будет заугружен и с которой можно будет начать в случаи остановки
        past_i_want_auction = past_i_want_auction + get_i_want_auction
        logging.warning(f"====="
                        f"Установить индекс в случаи ошибки {past_i_want_auction} "
                        f"| Загружаемый список {list_for_request}"
                        f"===============================================\n")
        # вызов функции
        main(count_create_task=count_create_task, list_for_request=list_for_request, type_work=type_work)
        safety_cancel(safe_canc, list_for_request, past_i_want_auction)

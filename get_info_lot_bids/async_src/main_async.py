import asyncio
import datetime
import logging
import time
import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from get_info_lot_bids.async_src.get import gather_data
# from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction # TODO: раскоммитить для нормальной работы
from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction_loss
from src.note_finally_parser import push_note_mail

# start_time = time.time()
# start_main = datetime.datetime.now()
# print(start_time)
logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


# Затраченное на работу скрипта время: 425.98178791999817 (на 1 аукцион 1985)
def main(count_create_task, list_for_request):
    start_main = datetime.datetime.now()
    start_time = time.time()
    logging.warning(f"====="
                    # f"Начало скрипта {start_time}"
                    f"Начало скрипта {start_main}"
                    f"=====\n")
    asyncio.run(gather_data(count_create_task, list_for_request))
    finish_time = time.time() - start_time
    finish_main = datetime.datetime.now() - start_main
    print(f"Затраченное на работу скрипта время: {finish_time}")
    logging.warning(f"====="
                    f"Затраченное время на скрипт сек: {finish_time}"
                    f"Конец скрипта:{finish_main}"
                    f"=====\n")


# def main_test(list_for_request):
#     print(list_for_request)
#     # time.sleep(10)
#     return 1


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
    past_i_want_auction = 350  # 1175
    get_i_want_auction = 1
    safe_canc = 180
    logging.warning(f"====="
                    f"Создано воркеров {count_create_task} "
                    f"| Установлен индекс {past_i_want_auction} "
                    f"| Загружается аукционов {get_i_want_auction} "
                    f"| Задержка safe cancel {safe_canc}"
                    f"=====\n")
    list_id_auction = list_id_hidden_auction_loss[:]
    count_length = len(list_id_auction) - past_i_want_auction
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
        main(count_create_task=count_create_task, list_for_request=list_for_request)
        # main_test(list_for_request=list_for_request)
        safety_cancel(safe_canc, list_for_request, past_i_want_auction)

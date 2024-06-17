import asyncio
import datetime
import logging
import time

from get_info_lot_bids.async_src.get import gather_data
from get_info_lot_bids.async_src.help_for_request.list_id_auction import list_id_hidden_auction
from src.note_finally_parser import push_note_mail

start_time = time.time()
start_main = datetime.datetime.now()
print(start_time)
logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


# Затраченное на работу скрипта время: 425.98178791999817 (на 1 аукцион 1985)
def main(count_create_task, list_for_request):
    logging.warning(f"\n===============================================\n"
                    f"Начало скрипта {start_time}"
                    f"Начало скрипта {start_main}"
                    f"\n===============================================\n")
    asyncio.run(gather_data(count_create_task, list_for_request))
    finish_time = time.time() - start_time
    finish_main = datetime.datetime.now() - start_main
    print(f"Затраченное на работу скрипта время: {finish_time}")
    logging.warning(f"\n===============================================\n"
                    f"Конец скрипта {finish_time}"
                    f"Конец скрипта {finish_main}"
                    f"\n===============================================\n")
    # return 1


def main_test(list_for_request):
    print(list_for_request)
    # time.sleep(10)
    return 1


def get_slice_id_auction(get_i_want_auction, past_i_want_auction, list_id_auction):
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
    count_create_task = 5
    past_i_want_auction = 104
    get_i_want_auction = 5
    safe_canc = 120
    logging.warning(f"\n===============================================\n"
                    f"\nСоздать воркеров {count_create_task}\n"
                    f"Последний индекс списка загруженный в бд {past_i_want_auction}\n"
                    f"Хочу при каждой итерации сгружать аукцинов {get_i_want_auction}\n"
                    f"Установлена задержка безопасного отключения {safe_canc}\n"
                    f"\n===============================================\n")
    list_id_auction = list_id_hidden_auction[:]
    count_length = len(list_id_auction) - past_i_want_auction
    count_iter = int(count_length / get_i_want_auction)
    for x in range(count_iter):
        list_for_request = get_slice_id_auction(get_i_want_auction, past_i_want_auction, list_id_auction)
        past_i_want_auction = past_i_want_auction + get_i_want_auction
        main(count_create_task=count_create_task, list_for_request=list_for_request)
        safety_cancel(safe_canc, list_id_auction, past_i_want_auction)

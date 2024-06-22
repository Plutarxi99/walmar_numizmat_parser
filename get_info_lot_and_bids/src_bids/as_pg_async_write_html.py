import datetime
import logging
import sys
import time

import asyncpg

from config import settings
from get_info_lot_and_bids.src_bids import models_bids
from get_info_lot_and_bids.src_bids.database_conf import engine_bids, SessionBids
from get_info_lot_and_bids.src_bids.models_bids import HtmlStr
from note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


async def add_html_str_pg_asyncpg(data, type_work="asyncpg") -> None:
    """
    Функция для записи в базу данных
    Имеет два режима работы
    sqllite3 - служит для быстрого запуска кода(теряется скорость загрузки данных)
    asyncpg - служит для быстрой радоты кода(требуется устновка на комп postgresql)
    :param data: список словарей [{"response_text": str,  "id_lot": int, "id_auction": int}, {}]
    :param type_work: <sqllite3> | <asyncpg>
    :return: None
    """
    try:
        if type_work == settings.TYPE_WORK:
            models_bids.BaseBids.metadata.create_all(bind=engine_bids)
            list_data_for_insert = []
            for tuple_item in data:
                dict_data_in_db = {
                    "html": tuple_item[0],
                    "id_lot_hidden": tuple_item[1],
                    "id_auction_hidden": tuple_item[2],
                }
                list_data_for_insert.append(dict_data_in_db)
            with SessionBids() as session:
                session.bulk_insert_mappings(HtmlStr, list_data_for_insert)
                session.commit()
        # elif type_work == "asyncpg":
        else:
            conn = await asyncpg.connect(settings.SQLALCHEMY_DATABASE_URL_POSTGRES)
            await conn.executemany(f'''
                        INSERT INTO {settings.POSTGRES_TABLE}(html, id_lot_hidden, id_auction_hidden) VALUES($1, $2, $3)
                    ''', data)

            await conn.close()
    except Exception as e:
        date_wrong = datetime.datetime.now()
        logging.error(f"[{date_wrong}]"
                      f"Проблема c записью в бд: {e}"
                      f"===============================================")
        push_note_mail(email_text=f"Упала ошибка. Проблема с записью в бд {e}",
                       subject_email="Проблема с бд")
        print(f"{e}"
              "Уходит в сон. остановилось в бд")
        sys.exit()

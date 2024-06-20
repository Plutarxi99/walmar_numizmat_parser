import datetime
import logging
import sys
import traceback

import asyncpg

from config import settings
from src.note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


async def add_record_pg_asyncpg(data, id_hidden_lot):
    try:
        conn = await asyncpg.connect(settings.SQLALCHEMY_DATABASE_URL_POSTGRES)
        for d in data:
            id_hidden_lot = int(id_hidden_lot)
            amount_bid = int(d['amount_bid'])
            nickname = d['nickname']
            datetime_pay = d['datetime_pay']
            status = d['status']
            try:
                uniq_str = d['uniq_str']
            except Exception as e:
                uniq_str = str(id_hidden_lot)[1:] + "_" + str(id_hidden_lot)[:-1] + "_" + str(id_hidden_lot)[2:]

            await conn.execute('''
                INSERT INTO bids(id_hidden_lot, amount_bid, nickname, datetime_pay, status, uniq_str) VALUES($1, $2, $3, $4, $5, $6)
            ''', id_hidden_lot, amount_bid, nickname, datetime_pay, status, uniq_str)

        await conn.close()
    except asyncpg.exceptions.UniqueViolationError:
        pass
    except Exception as e:
        date_wrong = datetime.datetime.now()
        logging.error(f"[{date_wrong}]"
                      f"Проблема c записью в бд: {e}"
                      f"{traceback.format_exc()}")
        push_note_mail(email_text=f"Упала ошибка. Проблема с записью в бд {e}",
                       subject_email="Проблема с бд")
        sys.exit()



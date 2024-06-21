import datetime
import logging
import sys
import time
import traceback

import asyncpg

from config import settings
from src.note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


# async def add_html_str_pg_asyncpg(html, id_lot_hidden, id_auction_hidden, try_connect):
async def add_html_str_pg_asyncpg(data, try_connect):
    if try_connect:
        try:
            conn = await asyncpg.connect(settings.SQLALCHEMY_DATABASE_URL_POSTGRES)
            # await conn.execute('''
            #             INSERT INTO html_str_3(html, id_lot_hidden, id_auction_hidden) VALUES($1, $2, $3)
            #         ''', html, id_lot_hidden, id_auction_hidden)
            await conn.executemany('''
                        INSERT INTO html_str_4(html, id_lot_hidden, id_auction_hidden) VALUES($1, $2, $3)
                    ''', data)

            await conn.close()
            # pool = await asyncpg.create_pool(settings.SQLALCHEMY_DATABASE_URL_POSTGRES, min_size=10, max_size=10,
            #                                  max_inactive_connection_lifetime=300.0)
            # async with pool.acquire() as conn:
            #     # async with conn.transaction():
            #     # await conn.execute('''
            #     #                         INSERT INTO html_str_3(html, id_lot_hidden, id_auction_hidden) VALUES($1, $2, $3)
            #     #                      ''', html, id_lot_hidden, id_auction_hidden)
            #     await conn.execute_many(
            #         'INSERT INTO mytable (html, id_lot_hidden, id_auction_hidden) VALUES ($1, $2, $3)',
            #         data
            #     )
            # return True
        except Exception as e:
            date_wrong = datetime.datetime.now()
            logging.error(f"[{date_wrong}]"
                          f"Проблема c записью в бд: {e}"
                          # f"{traceback.format_exc()}"
                          f"===============================================")
            push_note_mail(email_text=f"Упала ошибка. Проблема с записью в бд {e}",
                           subject_email="Проблема с бд")
            print(f"{e}"
                  "Уходит в сон. остановилось в бд")
            time.sleep(20)
            try_connect = False
            sys.exit()
            # return False
    else:
        pass

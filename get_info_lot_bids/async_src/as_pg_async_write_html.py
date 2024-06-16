import datetime
import logging
import sys
import traceback

import asyncpg

from config import settings
from src.note_finally_parser import push_note_mail

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


async def add_record_pg_asyncpg(data, id_hidden_lot):
        conn = await asyncpg.connect(settings.SQLALCHEMY_DATABASE_URL_POSTGRES)
        await conn.execute('''
            INSERT INTO bids(html, id_hidden_lot) VALUES($1, $2)
        ''', data, id_hidden_lot)

        await conn.close()


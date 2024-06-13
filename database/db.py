# import sqlite3
# from datetime import datetime

from peewee import *

from config import settings
from src.parser_data import test_data_for_db_all_page

# db = SqliteDatabase

# def connect_to_db(name_bd):
#     conn = sqlite3.connect(f'{name_bd}')
#     return conn


# class ConnAndCRUD:
#     def __init__(self, name_bd):
#         self._conn = SqliteDatabase(f'{name_bd}',
#                                     pragmas={
#                                         'journal_mode': 'wal', # позволяет читателям и писателям сосуществовать
#                                     })
#
#     def create_table_storage_coin(self):
#         pass
#
#     def status_db(self):
#         return self._conn.is_closed()
#
#     def close_conn_to_db(self):
#         close = self._conn.close()
#         return close

# with SqliteDatabase(settings.PATH_TO_DB) as db:
#     # Определяем базовую модель о которой будут наследоваться остальные
#     class BaseModel(Model):
#         class Meta:
#             database = db  # соединение с базой, из шаблона выше
#
#     # (number_in_site, title_lot, year_coin, mint, metal_gr, safety, buyer, bids, amount, status, full_url)
#     # Определяем модель исполнителя
#     class LotAuction(BaseModel):
#         lot_id = AutoField(column_name='lot_id')
#         # number_in_site = SmallIntegerField(column_name='Int_on_site')
#         title_lot = FixedCharField(max_length=100, column_name='title')
#         year_coin = SmallIntegerField(column_name='year')
#         mint = FixedCharField(max_length=30, null=True, column_name='mint')
#         metal_gr = FixedCharField(max_length=30, null=True, column_name='metal_gr')
#         safety = FixedCharField(max_length=30, null=True, column_name='safety')
#         buyer = FixedCharField(max_length=50, null=True, column_name='buyer')
#         bids = SmallIntegerField(column_name='bids')
#         amount = IntegerField(column_name='amount')
#         status = FixedCharField(max_length=30, null=True, column_name='status')
#         full_url = FixedCharField(max_length=150, null=True, column_name='url', unique=True)
#
#         class Meta:
#             table_name = 'lot_action'
#
#
#     print(db.create_tables([LotAuction]))
#     print(db.table_exists(LotAuction))


    # LotAuction.insert_many(test_data_for_db_all_page).execute()
def add_in_db_many_value(class_model: Model, data: dict):
    class_model.insert_many(data).execute()
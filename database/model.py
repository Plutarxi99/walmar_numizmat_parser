# # Определяем базовую модель о которой будут наследоваться остальные
# from peewee import *
#
#
# class BaseModel(Model):
#     class Meta:
#         database = db  # соединение с базой, из шаблона выше
#
#
# # (number_in_site, title_lot, year_coin, mint, metal_gr, safety, buyer, bids, amount, status, full_url)
# # Определяем модель исполнителя
# class LotAuction(BaseModel):
#     lot_id = AutoField(column_name='lot_id')
#     # number_in_site = SmallIntegerField(column_name='Int_on_site')
#     title_lot = FixedCharField(max_length=100, column_name='title')
#     year_coin = SmallIntegerField(column_name='year')
#     mint = FixedCharField(max_length=30, null=True, column_name='mint')
#     metal_gr = FixedCharField(max_length=30, null=True, column_name='metal_gr')
#     safety = FixedCharField(max_length=30, null=True, column_name='safety')
#     buyer = FixedCharField(max_length=50, null=True, column_name='buyer')
#     bids = SmallIntegerField(column_name='bids')
#     amount = IntegerField(column_name='amount')
#     status = FixedCharField(max_length=30, null=True, column_name='status')
#     full_url = FixedCharField(max_length=150, null=True, column_name='url', unique=True)
#
#     class Meta:
#         table_name = 'lot_action'

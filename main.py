from datetime import datetime
from time import sleep

from peewee import *

from config import settings

from src.get_data import get_data_from_page_pass_test, get_data_from_page
from src.parser_data import get_soup_parser, parser_info_auction, parser_table_info

if __name__ == "__main__":
    html_str_static = get_data_from_page_pass_test('data_test/test_history_auction_all_page.html')
    soup_static = get_soup_parser(data=html_str_static)
    # list_auction_number_vip_static = get_all_number_auction()
    list_auction_number_vip_static = ['1983', '1980']
    info_auction_generally_static = parser_info_auction(soup_static)
    # data_info_lot = parser_table_info(soup)

    for number_auction in list_auction_number_vip_static:
        list_category = info_auction_generally_static['category_auction']
        # for category_auction in list_category:
        # https://www.wolmar.ru/auction/1983/monety-antika-srednevekove
        # url_on_auction = settings.URL_DOMEN + '/auction/' + number_auction + '/' + category_auction + '?all=1'
        url_on_auction = settings.URL_DOMEN + '/auction/' + number_auction + '?all=1'

        html_str = get_data_from_page(url_on_auction)
        soup = get_soup_parser(data=html_str)
        info_auction_generally = parser_info_auction(soup)
        data_info_lot = parser_table_info(soup, category_auction='')
        print(f"Записываем в базу данных {info_auction_generally['title_auction']}")
        with SqliteDatabase(settings.PATH_TO_DB) as db:
            # Определяем базовую модель о которой будут наследоваться остальные
            class BaseModel(Model):
                class Meta:
                    database = db  # соединение с базой, из шаблона выше


            # Определяем модель исполнителя
            class LotAuction(BaseModel):
                lot_id = AutoField(column_name='lot_id')
                # number_in_site = SmallIntegerField(column_name='Int_on_site')
                title_lot = FixedCharField(max_length=250, column_name='title')
                year_coin = SmallIntegerField(column_name='year')
                mint = FixedCharField(max_length=30, null=True, column_name='mint')
                metal_gr = FixedCharField(max_length=30, null=True, column_name='metal_gr')
                safety = FixedCharField(max_length=30, null=True, column_name='safety')
                buyer = FixedCharField(max_length=50, null=True, column_name='buyer')
                bids = SmallIntegerField(column_name='bids')
                amount = IntegerField(column_name='amount')
                status = FixedCharField(max_length=30, null=True, column_name='status')
                type_category = FixedCharField(max_length=100, null=True, column_name='type_category')
                full_url = FixedCharField(max_length=150, null=True, column_name='url', unique=True)

                class Meta:
                    table_name = settings.NAME_TABLE


            table_is_create_lot = db.table_exists(LotAuction)
            if table_is_create_lot is False:
                db.create_tables([LotAuction])


            class Auction(BaseModel):
                auction_id = AutoField(column_name='auction_id')
                title_auction = FixedCharField(max_length=100, column_name='title')
                date_closed = FixedCharField(max_length=40, column_name='date_closed')
                url = FixedCharField(max_length=150, column_name='url')

                class Meta:
                    table_name = 'action'


            table_is_create_auction = db.table_exists(Auction)
            if table_is_create_auction is False:
                db.create_tables([Auction])

            # add_in_db_many_value(LotAuction, data_info_lot)
            try:
                LotAuction.insert_many(data_info_lot).execute()
            except Exception as e:
                now = datetime.now()
                print(f"Ошибка обработана и записана в логи время: {now}")
                where_problem = 'LotAuction.insert_many(data_info_lot).execute()'
                cannot_write = info_auction_generally['title_auction']
                info_log = f'[{now}] -- [{where_problem}] -- [Не смог записать аукцион с названием {cannot_write}; url: {url_on_auction}] -- [{e}]\n'
                with open("data_test/log.txt", 'a') as txt:
                    txt.write(info_log)
                continue
            # print(LotAuction.get(lot_id=458))

# ==============================================
# 1. Подключаем библиотеки Python
# ==============================================
import psycopg2
import csv

from config import settings

# ==============================================
# 2. Подключаемся к базе данных PGSQL
# ==============================================
conn = psycopg2.connect(dbname=settings.POSTGRES_DB, user=settings.POSTGRES_USER,
                        password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_SERVER)
# ==============================================
# 3. Получаем данные, кладем их в курсор
# ==============================================
cursor = conn.cursor()
# cursor.execute(f'select id, id_hidden_lot, amount_bid, nickname, datetime_pay, status from {settings.POSTGRES_TABLE}')
cursor.execute(f'select * from {settings.NAME_TABLE_HTML}')
# --- Получаем наименования колонок
column_names = []
for row in cursor.description:
    column_names.append(row[0])
# ==============================================
# 4. Пишем файл CSV с колонками
# ==============================================
with open('bids_csv.csv', 'w', newline='') as filename:
    write_filename = csv.writer(filename, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_filename.writerow(column_names)
    for row in cursor:
        write_filename.writerow(row)
# ==============================================
# 5. Закрываем курсор
#    Закрываем соединение с Базой данных
# ==============================================
cursor.close()
conn.close()

import sqlite3
import csv
from pathlib import Path

from config import settings
"""Для преобразование бд в csv файл. Требует только запуска этого файла
Каждый раз создает новый файл. Перезаписывает раннее созданный такой же файл
"""
BASE_DIR = Path(__file__).resolve().parent.parent
path_to_db = settings.PATH_TO_DB
path_to_csv = BASE_DIR / settings.NAME_CSV


if __name__ == "__main__":
    # Подключение к базе данных SQLite
    with sqlite3.connect(path_to_db) as conn:
        cursor = conn.cursor()
        # Выполнить SQL-запрос
        query = f"SELECT * FROM {settings.NAME_TABLE}"
        cursor.execute(query)
        data = cursor.fetchall()

        # Записать данные в CSV-файл
        with open(path_to_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0] for i in cursor.description])
            writer.writerows(data)

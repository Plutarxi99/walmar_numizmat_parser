import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Settings:
    # Настройка используется в основном для получение лотов с аукционов
    PATH_TO_DB = BASE_DIR / os.getenv('PATH_TO_DB')
    PATH_TO_DB_LOSS = BASE_DIR / os.getenv('PATH_TO_DB_LOSS')
    URL_DOMEN = os.getenv('URL_DOMEN')
    NAME_BD = os.getenv('PATH_TO_DB')
    NAME_CSV = os.getenv('NAME_CSV')
    NAME_TABLE = os.getenv('NAME_TABLE')
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{PATH_TO_DB}"
    SQLALCHEMY_DATABASE_URL_LOSS = f"sqlite:///{PATH_TO_DB_LOSS}"
    # Настройка для получение электроного письма
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    SERVER_EMAIL = os.getenv('SERVER_EMAIL')
    SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
    # Настройки для асинхронной записи
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_DRIVER: str = os.getenv("POSTGRES_DRIVER")  # postgresql+asyncpg
    POSTGRES_TABLE: str = os.getenv("POSTGRES_TABLE")
    POSTGRES_DRIVER_SINHR: str = os.getenv("POSTGRES_DRIVER_SINHR")
    NAME_TABLE_HTML: str = os.getenv("NAME_TABLE_HTML")

    SQLALCHEMY_DATABASE_URL_POSTGRES: str = f"{POSTGRES_DRIVER}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    # SQLALCHEMY_DATABASE_URL_POSTGRES_SHORT: str = f"{POSTGRES_DRIVER_SINHR}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    NAME_DB_BIDS: str = os.getenv("NAME_DB_BIDS")
    PATH_TO_DB_BIDS: str = BASE_DIR / NAME_DB_BIDS
    SQLALCHEMY_DATABASE_URL_SQLITE_FOR_BIDS: str = f"sqlite:///{PATH_TO_DB_BIDS}"
    TYPE_WORK: str = os.getenv("TYPE_WORK_ASYNC")


settings = Settings()

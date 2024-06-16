import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


# load_dotenv('.env')


class Settings:
    PATH_TO_DB = BASE_DIR / os.getenv('PATH_TO_DB')
    URL_DOMEN = os.getenv('URL_DOMEN')
    NAME_BD = os.getenv('PATH_TO_DB')
    NAME_CSV = os.getenv('NAME_CSV')
    NAME_TABLE = os.getenv('NAME_TABLE')
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{PATH_TO_DB}"
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    SERVER_EMAIL = os.getenv('SERVER_EMAIL')
    SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_DRIVER: str = os.getenv("POSTGRES_DRIVER") # postgresql+asyncpg
    POSTGRES_TABLE: str = os.getenv("POSTGRES_TABLE")

    SQLALCHEMY_DATABASE_URL_POSTGRES: str = f"{POSTGRES_DRIVER}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

    PROXIES_IP_DEF = os.getenv("PROXIES_IP_DEF")
    PROXIES_PORT_DEF = os.getenv("PROXIES_PORT_DEF")
    PROXIES_IP = os.getenv("PROXIES_IP")
    PROXIES_PORT = os.getenv("PROXIES_PORT")
    PROXIES_EMAIL = os.getenv("PROXIES_EMAIL")
    PROXIES_PASS = os.getenv("PROXIES_PASS")

settings = Settings()

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


settings = Settings()

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
# load_dotenv('.env')


class Settings:
    PATH_TO_DB = BASE_DIR / os.getenv('PATH_TO_DB')
    URL_DOMEN = os.getenv('URL_DOMEN')


settings = Settings()


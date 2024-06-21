import logging
import smtplib
import traceback
from datetime import datetime
from email.mime.text import MIMEText

from transliterate import translit

from config import settings

logging.basicConfig(level=logging.WARNING, filename="log_async.log", filemode="a")


def push_note_mail(email_text: str, subject_email: str = 'Парсер сайта нумизматики'):
    try:
        msg = MIMEText(email_text)
        msg['Subject'] = subject_email
        msg['From'] = (f'Parser cannot work '
                       f'<{settings.SERVER_EMAIL}>')
        msg['To'] = settings.ADMIN_EMAIL
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(settings.SERVER_EMAIL, settings.SERVER_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        date_wrong = datetime.now()
        logging.error(f"[{date_wrong}]"
                      f"Проблема в получении запроса {e}"
                      f"{traceback.format_exc()}"
                      f"===============================================")

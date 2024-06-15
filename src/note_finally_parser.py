import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from transliterate import translit

from config import settings


def push_note_mail(email_text: str, subject_email: str = 'Парсер сайта нумизматики'):
    msg = MIMEText(email_text)
    msg['Subject'] = subject_email
    msg['From'] = (f'Parser cannot work '
                   f'<{settings.SERVER_EMAIL}>')
    msg['To'] = settings.ADMIN_EMAIL
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(settings.SERVER_EMAIL, settings.SERVER_PASSWORD)
    server.send_message(msg)
    server.quit()

    # email = settings.SERVER_EMAIL
    # password = settings.SERVER_PASSWORD
    #
    # server = smtplib.SMTP('smtp.yandex.ru', 587)
    # server.ehlo()
    # server.starttls()
    # server.login(email, password)
    #
    # admin_email = settings.ADMIN_EMAIL
    # m = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email, admin_email, subject_email, email_text)
    # message = translit(m, language_code='ru', reversed=True)
    # # server.set_debuglevel(1)  # Необязательно; так будут отображаться данные с сервера в консоли
    # server.sendmail(email, admin_email, message)
    # server.quit()

# start = datetime.now()
# time_work = f"Парсинг окончен {datetime.now() - start}"
# print(time_work)
# push_note_mail(email_text=time_work, subject_email="Время работы парсера")
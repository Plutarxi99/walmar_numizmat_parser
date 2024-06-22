# Walmar_numizmat_parser
Приложение для сбора информации по аукиционам и их лотам.

<details>

<summary>Данный проект содержит в себе 2 папке с разными скриптами:</summary>

* # **get_info_auction_and_lot**
   - Используется синхронный подход в программирование.
   - Используется для распарсивание страницы beautifulsoup4.
   - Объединено все в один процесс: запрос, парсим и записываем готовые данные в базу.
   - С помощью отдельного модуля получаем csv файл.
   - Позволяет получать базу данных с полями:

![Screenshot from 2024-06-22 11-37-52](https://github.com/Plutarxi99/walmar_numizmat_parser/assets/132927381/c74bdb5b-d65a-4799-9045-e7435ae2a8c8)


| Поле | Описание |
|-----|----------|
|     **lot_id**| порядковый номер в бд|
|     **title_lot**| название лота на русском языке        |
|     **year_coin**|год производства монеты|
|     **mint**|монетный двор|
|     **metal_gr**|метал и проба или вес|
|     **safety**|сохранность монеты|
|     **buyer**|покупатель монеты|
|     **bids**|количество хотевших купить монеты|
|     **amount**|финальная сумма покупки|
|     **status**|статус аукциона на монету|
|     **type_auction**|тип аукциона (std \ vip)|
|     **id_auction_hidden**|числовое значение в url адреса сайта аукциона|
|     **id_auction_visible**|числовое значение аукиона на сайте|
|     **id_lot_hidden**|числовое значение лота в url адреса|
|     **date_closed**|дата закрытия аукиона|
|     **full_url**|полная ссылка на лот|


* # **get_info_lot_and_bids**
   - Используется асинхронный подход.
   - Метод заключается в равном делении лотов в аукционе на части и их паралленую загрузка в бд.(Только если используется метод asyncpg)
   - Изначально мы парсим страницы и записываем сырую страницу в бд.
   - Из бд мы получаем этот материал и записыва в csv файл.
   - Ключевая особенность, что нет уникального значения. Задумка в максимальном сокращеннии времени по получению данных.
   - Парсер используется LexborHTMLParser. Самый быстрый парсер.
   - Позволяет получать базу данных с полями:

![Screenshot from 2024-06-22 11-55-49](https://github.com/Plutarxi99/walmar_numizmat_parser/assets/132927381/ec08359f-b639-4bfc-99fc-f8b7b5d552cf)

| Поле | Описание |
|-----|----------|
|     **id**| порядковый номер в бд|
|     **html**| html страница полученная путем запроса|
|     **id_hidden_auction**| числовое значение в url адреса сайта аукциона |
|     **id_hidden_lot**| числовое значение лота в url адреса |

![Screenshot from 2024-06-22 12-08-54](https://github.com/Plutarxi99/walmar_numizmat_parser/assets/132927381/441ecc3e-9e68-46c1-8828-41dc6640030e)

| Поле | Описание |
|-----|----------|
|     **id**| порядковый номер в бд|
|     **id_hidden_auction**| числовое значение в url адреса сайта аукциона |
|     **id_hidden_lot**| числовое значение лота в url адреса |
|     **amount_bid**|сумма ставки|
|     **nickname**|ник человека, который поставил ставку|
|     **datetime_pay**|дата и время ставки человека|
|     **status**|статут платежа (final[последняя ставка] \ inter[intermedia, промежуточная ставка] \ first[первая ставка])|

</details>

<details>

<summary>Что делает приложение?</summary>
Функционал:

* С помощью в скриптов get_info_auction_and_lot/main_auction.py и get_info_lot_and_bids/main_bids.py. Запускается парсинг требуемой информации.
* Запись в бд полученных данных и их преобразование в нужный вид.
* Запись результатов в csv файла.


</details>

> [!IMPORTANT]
> Добавлен файл .env-sample (для использования надо привести к ввиду **<.env>**) с помощью, которого можно настроить работу проекта. В нем лежат настройки (далее идут примеры заполнения полей):
<details>
<summary>Настройки, которые надо установить для работы приложения</summary>

| Значение | Содержание | Примечание |
|-----|-----------|-----:|
|     **PATH_TO_DB**| storage_coin.db   |     имя базы данных для get_info_auction_and_lot |
|     **URL_DOMEN**| https://www.wolmar.ru   |     название сайта откуда будет парсится |
|     **NAME_CSV**| storage_lot.csv  |     имя файлы csv для get_info_auction_and_lot |
|     **NAME_TABLE**| lot_action   |     название таблице в бд для get_info_auction_and_lot |
|     **ADMIN_EMAIL**| your_email@better.you       |     почта куда будут присылаться ссобщения|
|     **SERVER_EMAIL**| your_email@better.you        |     почта от кого будет присылаться сообщения|
|     **SERVER_PASSWORD**| q@W!e23231       |     пароль от сервиса|
|     **POSTGRES_USER**| name_user   |     для исполльзования асинхронности |
|     **POSTGRES_PASSWORD**|  password_user   |     для исполльзования асинхронности |
|     **POSTGRES_SERVER**| localhost  |     для исполльзования асинхронности|
|     **POSTGRES_DRIVER**| postgresql       |     для исполльзования асинхронности|
|     **POSTGRES_DB**| name_bd       |для исполльзования асинхронности|
|     **POSTGRES_TABLE**| name_table      |для исполльзования асинхронности|
|     **NAME_DB_BIDS**| storage_html_str_bids.db   |     дефолтные настройки для почтового сервиса в моем случае это яндекс|
|     **TYPE_WORK**| sqllite3 | asyncpg    |     база данных для работы celery|
</details>

<details>

<summary>Как запустить?</summary>

* Переходим в папку где будет лежать код

* Копируем код с git:
  <pre><code>git clone git@github.com:Plutarxi99/walmar_numizmat_parser.git</code></pre>

* Переходим в папку:
  <pre><code>cd walmar_numizmat_parser/</code></pre>

* Создаем виртуальное окружение:
  <pre><code>python3 -m venv env</code></pre>
  <pre><code>source env/bin/activate</code></pre>

* Если не будешь использовать асинхронность, то пропусти шаги:
  - Создать базу данных:
  - <pre><code>psql -U postgres</code></pre>
  - <pre><code>create name_bd;</code></pre>
  - Создать таблицу:
  - <pre><code>CREATE TABLE name_table(id SERIAL PRIMARY KEY,html TEXT,id_lot_hidden integer,id_auction_hidden integer);</code></pre>

* После установки нужных настроук в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt</code></pre>
</details>

<details>

<summary>Запуск модуля get_info_auction_and_lot</summary>

* Открываем файл get_info_auction_and_lot/storage_file/last_iter.txt и вставляем туда id аукциона, который есть в url и от него начнется парсинг. К примеру, ставим 1987. А спарсим мы страницы аукционов [1987, 1989, 1990]

* Запускаем парсинг:
  - <pre><code>cd get_info_auction_and_lot/</code></pre>
  - <pre><code>python3 main_auction.py</code></pre>

* Запускаем перевод в csv файл:
  - <pre><code>cd src_auction/</code></pre>
  - <pre><code>python3 translation_from_db_in_csv.py</code></pre>

* Все порлученные данные лежат в корне проекта.

</details>

<details>

<summary>Запуск модуля get_info_lot_and_bids</summary>

* В начале нам надо поулчить начальные данные, что запустить парсинг:
  - <pre><code>cd get_info_lot_and_bids/</code></pre>
  - <pre><code>python3 pre_start.py</code></pre>
* Полученный результат копируем:
  - Список копируем: help_for_request_bids/list_id_auction.py
  - Словарь копируем: help_for_request_bids/dict_data_auction_lot.py

![Screenshot from 2024-06-22 13-16-30](https://github.com/Plutarxi99/walmar_numizmat_parser/assets/132927381/8ad734dd-5c33-4d61-b7a9-3ad6d2566a4b)

  - (Не объзательно)Добавить в get_info_lot_and_bids/help_for_request_bids/list_proxies_static.py этот файл, чтобы с него подгружались ip-прокси с названием словаря list_proxies_static.
  - К примеру,
  - list_proxies_static = ['http://111.111.111.111:9999', 'http://111.111.111.111:9999']
  - (Не объзательно)Добавить в get_info_lot_and_bids/help_for_request_bids/list_user_agent_static.py этот файл, чтобы с него подгружались user-agent с названием словаря list_user_agent_static
  - К примеру,
  - list_user_agent_static = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.750 Yowser/2.5 Safari/537.36"},{"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

* В этом модуле можно узнать какой индекс имеет id аукциона в списке со всех аукционов. Имеет дело с реальным времен, то есть информация актуально на данный момент get_info_auction_and_lot/src_auction/get_index_for_parsing.py
  - можно после if __name__ == "__main__":
  - id_auction = 1989
  - поставить какой аукцион нужен. И от него будет парсится. Парсинг идет в обратную сторону. И ориетируется на список указзаный в help_for_request_bids/list_id_auction.py

![Screenshot from 2024-06-22 14-21-26](https://github.com/Plutarxi99/walmar_numizmat_parser/assets/132927381/74546589-ceb0-4a0d-a94f-729f11c9f14d)


* Запускуаем парсинг перед этим можно поставить настройки:
  - <pre><code>python3 main_bids.py</code></pre>

* Запускаем перевод в csv файл:
  - <pre><code>cd src_auction/</code></pre>
  - <pre><code>python3 translation_from_db_in_csv.py</code></pre>

* Все порлученные данные лежат в корне проекта.

</details>

<details>

<summary>Как получить пароль почтового сервиса?</summary>
Функционал:

* Создать приложение по ссылке и создать приложение <<Почта>> и получить пароль:
  https://id.yandex.ru/security/app-passwords
![Screenshot from 2024-03-25 15-08-40](https://github.com/Plutarxi99/user_invite/assets/132927381/330bf584-9920-40a5-8324-5429f2d8ddc4)

* Скопировать пароль в .env файл оставльные настройка уже готовы.

</details>


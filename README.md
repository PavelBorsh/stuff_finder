# Stuff Finder

Агрегатор цен на смартфоны с 5 сайтов:
  - МТС
  - Мегафон
  - Ситилинк
  - Эльдорадо
  - Технопорт

Рабочую версию можно протестировать по адресу: [www.rattle.one][rttl]


### Установка

Тестировалось на Ubuntu 18.04.3 (LTS) x64

Перед установкой необходимо создать пользователя без привелегий root и с привелегиями sudo.

Установка приложения.

```sh
$ git clone https://github.com/PavelBorsh/stuff_finder.git
$ cd stuff_finder
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Установка PostgreSQL

```sh
$ sudo apt update
$ sudo apt install postgres
$ sudo apt install python-psycopg2
$ apt install libpq-dev
```
### Настройка базы данных

Установка пароля доступа.

```sh
$ su
$ su - postgres
$ psql
$ \password
```
Создание базы данных.

```sh
$ su
$ su - postgres
$ psql
$ CREATE DATABASE имя_базы
```

Вместо stuff_finder можно указать любое корректное имя для базы данных, но по умолчанию в конфиге прописано название базы данных 'stuff_finder'.

Доступ к базе извне (при помощи pgAdmin):
- В файле postgresql.conf (по умолчанию находится в /etc/postgresql/...) прописать: listen_addresses = '*'
- host all             all             0.0.0.0/0            md5

### Добавление магазинов, парсинг цен и характеристик.

Перед запуском приложения необходимо создать записи магазинов в базе данных и спарсить характеристики смартфонов. Характеристики парсятся с сайта МТС

```sh
$ python add_shops.py
$ python parse_specs.py

```

Теперь можно либо спарсить цены, либо запустить Celery и дождаться пока Celery запустит задания парсинга цен.

### Запуск приложения.

```sh
$ export FLASK_APP=webapp
$ flask run
```
### Настройка и запуск Celery

Установка Redis.

```sh
$ sudo apt install redis-server
$ sudo systemctl start redis-server
```
Запуск Celery.
Задачи прописаны в файле tasks.py.

```sh
$ celery -A tasks  worker -B --loglevel=info -f celery.log
```

[//]:


   [rttl]: <http://rattle.one>
  
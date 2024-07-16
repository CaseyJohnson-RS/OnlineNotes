# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import psycopg2
from .config import DATABASE_URI

conn = None

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(DATABASE_URI)
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def shutdown():

    conn.close()
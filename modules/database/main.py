# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import psycopg2
from .config import DATABASE_URI
from modules.logging.main import LogTime, Log
from psycopg2.extras import RealDictCursor

connection = None


def DBConnect():
    global connection

    LogTime()

    if not connection is None:
        connection.close()

    Log('Connect database...')

    try:
        # пытаемся подключиться к базе данных
        connection = psycopg2.connect(DATABASE_URI)
    except Exception as e:

        Log('Can`t establish connection to database')


def DBSession(func):
    
    def wrapper(*args, **kwargs):
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        result = func(*args, **kwargs,cursor=cursor)
        cursor.close()
        return result
    
    return wrapper


@DBSession
def send_fetch_query(query: str, query_values: tuple, fetch_type: str = 'one', cursor=None) -> object:

    try:
        cursor.execute(query, query_values)
    except Exception as e:

        LogTime()
        Log("DataBase Exception: " + str(e))

        DBConnect()

        return False
    
    result = None

    if fetch_type == 'one':
        result = cursor.fetchone()
    elif fetch_type == 'all':
        result = cursor.fetchall()

    if result == None:
        LogTime()
        Log("From DataBase Fetched 'None'. \nQuery:")
        Log(query)
        Log("Values:")
        Log(query_values)
    
    return result


@DBSession
def send_query(query: str, query_values: tuple, cursor=None) -> bool:

    try:
        cursor.execute(query, query_values)
        connection.commit()
    except Exception as e:  
        LogTime()
        Log("DataBase Exception: " + str(e))

        DBConnect()

        return False
     
    return True


DBConnect()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def shutdown():

    connection.close()
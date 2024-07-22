import psycopg2
from .config import DATABASE_URI
from modules.logging import Log
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor as Cursor


connection = None


def DBConnect():
    global connection

    if not connection is None:
        connection.close()

    Log("Connect database...")

    try:
        connection = psycopg2.connect(DATABASE_URI)
    except Exception as e:
        Log("Connection failed: " + str(e))
        return 
    
    Log("Сonnection successful")


def DBSession(func):
    
    def wrapper(*args, **kwargs):
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        result = func(*args, **kwargs,cursor=cursor)
        cursor.close()
        return result
    
    return wrapper


@DBSession
def send_fetch_query(query: str, query_values: tuple, fetch_type: str = 'one', cursor: Cursor = None) -> object:

    try:
        cursor.execute(query, query_values)
    except Exception as e:

        Log("DataBase Exception: " + str(e))

        DBConnect()

        return None
    
    result = None

    if fetch_type == 'one':
        result = cursor.fetchone()
    elif fetch_type == 'all':
        result = cursor.fetchall()
    
    return result


@DBSession
def send_query(query: str, query_values: tuple, cursor: Cursor = None) -> bool:

    try:
        cursor.execute(query, query_values)
        connection.commit()
    except Exception as e:  
        Log("DataBase Exception: " + str(e))

        DBConnect()

        return False
    
    data = cursor.fetchall()

    if not data is None:
        return data

    return True


DBConnect()
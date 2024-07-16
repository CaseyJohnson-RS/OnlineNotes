from psycopg2.extras import RealDictCursor

from .main import connection
from common.schemas import User

# В свое оправдание скажу, что базы данных проектировать я не умел до того
# Как начал этот проект. И осуждать меня за этот плохой API взаимодействия
# С базой данных не стоит. Лучше помогите материально(

def DBSession(func):
    
    def wrapper(*args, **kwargs):
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        result = func(*args, **kwargs,cursor=cursor)
        cursor.close()
        return result
    
    return wrapper

@DBSession
def get_user_by_username(username: str, cursor) -> User | None:

    cursor.execute("SELECT * FROM \"Users\" WHERE email=%s", (username,))
    user_data = cursor.fetchone()

    if user_data is None:
        return None

    cursor.execute("SELECT * FROM \"Roles\" WHERE id=%s", (user_data["role_id"],))
    role = cursor.fetchone()

    user = User(
        id = user_data["id"],
        email = user_data["email"],
        password_hash = user_data["password_hash"],
        active = user_data["active"],
        role = role["role_name"]
    )

    return user

@DBSession
def get_user_by_id(id: int, cursor) -> User | None:

    cursor.execute("SELECT * FROM \"Users\" WHERE id=%s", (id,))
    user_data = cursor.fetchone()

    if user_data is None:
        return None

    cursor.execute("SELECT * FROM \"Roles\" WHERE id=%s", (user_data["role_id"],))
    role = cursor.fetchone()

    user = User(
        id = user_data["id"],
        email = user_data["email"],
        password_hash = user_data["password_hash"],
        active = user_data["active"],
        role = role["role_name"]
    )

    return user


@DBSession
def get_password_hash_by_username(username: str, cursor) -> str | None:

    cursor.execute("SELECT password_hash FROM \"Users\" WHERE email=%s", (username,))
    data = cursor.fetchone()

    if data is None: 
        return None

    return data["password_hash"]


@DBSession
def get_user_id_by_username(username: str, cursor) -> int | None:

    cursor.execute("SELECT id FROM \"Users\" WHERE email=%s", (username,))
    data = cursor.fetchone()

    if data is None: 
        return None
    
    return data["id"]


@DBSession
def add_user(username: str, password_hash: str, nickname: str, active: bool, role: str, cursor) -> int | None:

    cursor.execute("SELECT id FROM \"Roles\" WHERE role_name=%s", (role,))
    data = cursor.fetchone()

    if data is None:
        return None
    
    role_id = data["id"]

    query = """
        INSERT INTO "Users" (email, nickname, password_hash, active, role_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    query_values = (username, nickname, password_hash, active, role_id)

    cursor.execute(query, query_values)
    connection.commit()

    cursor.execute("SELECT id FROM \"Users\" WHERE email=%s", (username,))

    return cursor.fetchone()["id"]

"""
@DBSession
def p(cursor):

    cursor.execute("SELECT role_name FROM \"Roles\" WHERE id=%s", (1,))
    t = cursor.fetchone()

    print(t)

p()"""
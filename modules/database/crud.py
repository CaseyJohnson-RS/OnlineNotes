from psycopg2.extras import RealDictCursor

from .main import connection
from common.schemas import User, Note

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

# - - - - - - - - - - - - Often use functions  - - - - - - - - - - - -

@DBSession
def get_user_data(user_id_or_name: str | int, cursor) -> dict | None:

    query = ""
    query_values = (user_id_or_name,)

    if type(user_id_or_name) is int: # It's id
        query = "SELECT * FROM \"Users\" WHERE id=%s"
    else: # It's username
        query = "SELECT * FROM \"Users\" WHERE email=%s"

    try: 
        cursor.execute(query, query_values)
        user_data = cursor.fetchone()
    except Exception:
        return None
    
    return user_data


def user_exists(user_id_or_name: str | int) -> bool:
    return not get_user_data(user_id_or_name) is None


@DBSession
def convert_role(role_name_or_id: str | int, cursor) -> int | str | None:

    query = ""
    key = ""
    query_values = (role_name_or_id,)
    
    if type(role_name_or_id) is int: # It's id

        query = "SELECT * FROM \"Roles\" WHERE id=%s"
        key = "role_name"

    else: # It's username
        query = "SELECT * FROM \"Users\" WHERE role_name=%s"
        key = "id"

    try:
        cursor.execute(query, query_values)
        role_data = cursor.fetchone()
    except Exception:
        return None
    
    if role_data is None:
        return None
    
    return role_data[key]


def get_username(user_id_or_name: str | int) -> str | None:

    user_data = get_user_data(user_id_or_name)

    if user_data is None:
        return None
    
    return user_data["email"]

# - - - - - - - - - - - - Authorization mainly used functions  - - - - - - - - - - - -

def get_user(user_id_or_name: str | int) -> User | None:

    user_data = get_user_data(user_id_or_name)

    if user_data is None:
        return None

    role_name = convert_role(user_data["role_id"])

    if role_name is None:
        return None
    
    user = User(
        id = user_data["id"],
        email = user_data["email"],
        password_hash = user_data["password_hash"],
        active = user_data["active"],
        role = role_name
    )

    return user


def get_user_password_hash(user_id_or_name: str | int) -> str | None:

    user_data = get_user_data(user_id_or_name)

    if user_data is None: 
        return None

    return user_data["password_hash"]


def get_user_id(username: str) -> int | None:

    user_data = get_user_data(username)

    if user_data is None: 
        return None
    
    return user_data["id"]


@DBSession
def add_user(username: str, password_hash: str, nickname: str, active: bool, role: str, cursor) -> int | None:

    role_id = convert_role(role)

    if role_id is None:
        return None

    query = """
        INSERT INTO "Users" (email, nickname, password_hash, active, role_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    query_values = (username, nickname, password_hash, active, role_id)

    try:
        cursor.execute(query, query_values)
        connection.commit()
    except Exception:
        return None
    
    cursor.execute("SELECT id FROM \"Users\" WHERE email=%s", (username,))

    return cursor.fetchone()["id"]


@DBSession
def update_password_hash(user_id_or_name: str | int, password_hash: str, cursor) -> None:

    query = ""
    query_values = (password_hash, user_id_or_name)

    if type(user_id_or_name) is int:
        query = """UPDATE "Users" SET password_hash = %s WHERE id = %s;"""
    else:
        query = """UPDATE "Users" SET password_hash = %s WHERE email = %s;"""

    try:
        cursor.execute(query, query_values)
        connection.commit()
    except Exception:
        return False
    
    return True

# - - - - - - - - - - - - NotesAPI mainly used functions  - - - - - - - - - - - -

@DBSession
def create_note_in_db(user_id: int, cursor) -> bool:

    query = """INSERT INTO "Notes" (user_id) VALUES (%s)"""
    query_value = (user_id,)

    try:
        cursor.execute(query, query_value)
        connection.commit()
    except Exception:
        return False
    
    return True


@DBSession
def convert_note_status(note_status_name_or_id: int | str, cursor) -> int | str | None:

    query = ""
    key=""
    query_values = (note_status_name_or_id,)

    if type(note_status_name_or_id) is int:
        query = """SELECT * FROM "Note_status" WHERE id=%s"""
        key="title"
    else:
        query = """SELECT * FROM "Note_status" WHERE title=%s"""
        key="id"
    
    try:
        cursor.execute(query, query_values)    
    except Exception:
        return None
    
    row = cursor.fetchone()

    if row is None:
        return None
    
    return row[key]


@DBSession
def get_note(user_id: int, note_id: int, cursor) -> Note | None:

    query = """SELECT * FROM "Notes" WHERE user_id = %s AND note_id = %s"""
    query_value = (user_id, note_id)

    note_data = None

    try:
        cursor.execute(query, query_value)
        note_data = cursor.fetchone()
    except Exception:
        return None 
    
    if note_data is None:
        return None
    
    note_status = convert_note_status(note_data["status"])

    if note_status is None:
        return None
    
    note = Note(
        note_id=note_id,
        header=note_data["header"],
        text = note_data["text"],
        hex_color = note_data["hex_color"],
        status = note_status
    )

    return note


@DBSession
def update_note_in_db(user_id: int, note: Note, cursor) -> bool:

    query = """
        UPDATE "Notes" SET header=%s, text=%s, hex_color=%s, status=%s 
        WHERE user_id=%s AND note_id=%s
    """

    new_note_status = convert_note_status(note.status)

    if new_note_status is None:
        return False

    query_value = ( note.header, note.text, note.hex_color, new_note_status, user_id, note.note_id)

    try:
        cursor.execute(query, query_value)
        connection.commit()
    except Exception:
        return False
    
    return True
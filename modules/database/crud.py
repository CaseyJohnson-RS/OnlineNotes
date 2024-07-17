

from .main import send_query, send_fetch_query
from common.schemas import User, Note

# В свое оправдание скажу, что базы данных проектировать я не умел до того
# Как начал этот проект. И осуждать меня за этот плохой API взаимодействия
# С базой данных не стоит. Лучше помогите материально(

# - - - - - - - - - - - - Often use functions  - - - - - - - - - - - -

def get_user_data(user_id_or_name: str | int) -> dict | None:

    query = "SELECT * FROM \"Users\" WHERE "
    query_values = (user_id_or_name,)

    query += "id=%s" if type(user_id_or_name) is int else "email=%s"

    user_data = send_fetch_query(query, query_values, 'one')
    
    return user_data


def user_exists(user_id_or_name: str | int) -> bool:
    return not get_user_data(user_id_or_name) is None


def convert_role(role_name_or_id: str | int) -> int | str | None:

    query = "SELECT * FROM \"Roles\" WHERE "
    key = ""
    query_values = (role_name_or_id,)
    
    if type(role_name_or_id) is int: # It's id
        query += "id=%s"
        key = "role_name"
    else: # It's username
        query += "role_name=%s"
        key = "id"

    role_data = send_fetch_query(query, query_values, 'one')

    return role_data and role_data[key]


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

    return user_data and user_data["password_hash"]


def get_user_id(username: str) -> int | None:

    user_data = get_user_data(username)
    
    return user_data and user_data["id"]


def add_user(username: str, password_hash: str, nickname: str, active: bool, role_name: str) -> int | None:

    role_id = convert_role(role_name)

    query = """
        INSERT INTO "Users" (email, nickname, password_hash, active, role_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    query_values = (username, nickname, password_hash, active, role_id)

    send_query(query, query_values)

    user_data = send_fetch_query("SELECT id FROM \"Users\" WHERE email=%s", (username,), 'one')
    
    return user_data["id"]


def update_password_hash(user_id_or_name: str | int, password_hash: str) -> bool:

    query = """UPDATE "Users" SET password_hash = %s WHERE """
    query_values = (password_hash, user_id_or_name)

    query += "id = %s;" if type(user_id_or_name) is int else "email = %s;"

    return send_query(query, query_values)

# - - - - - - - - - - - - NotesAPI mainly used functions  - - - - - - - - - - - -

def create_note_in_db(user_id: int) -> bool:

    query = """INSERT INTO "Notes" (user_id) VALUES (%s)"""
    query_value = (user_id,)

    return send_query(query, query_value)


def convert_note_status(note_status_name_or_id: int | str) -> int | str | None:

    query = """SELECT * FROM "Note_status" WHERE """
    key=""
    query_values = (note_status_name_or_id,)

    if type(note_status_name_or_id) is int:
        query += "id=%s"
        key="title"
    else:
        query += "title=%s"
        key="id"
    
    data = send_fetch_query(query, query_values)
    
    return data and data[key]


def get_note(user_id: int, note_id: int) -> Note:

    query = """SELECT * FROM "Notes" WHERE user_id = %s AND note_id = %s"""
    query_value = (user_id, note_id)

    note_data = send_fetch_query(query, query_value, 'one')
    note_status = convert_note_status(note_data["status"])
    
    note = Note(
        note_id=note_id,
        header=note_data["header"],
        text = note_data["text"],
        hex_color = note_data["hex_color"],
        status = note_status
    )

    return note


def update_note_in_db(user_id: int, note: Note) -> bool:

    new_note_status = convert_note_status(note.status)

    if new_note_status is None:
        return False

    query = """
        UPDATE "Notes" SET header=%s, text=%s, hex_color=%s, status=%s 
        WHERE user_id=%s AND note_id=%s
    """
    query_value = ( note.header, note.text, note.hex_color, new_note_status, user_id, note.note_id)
    
    return send_query(query, query_value)


def delete_note_in_db(user_id: int, note_id: int) -> bool:

    query = """
        DELETE FROM "Notes"
        WHERE user_id = %s AND note_id = %s
    """
    query_values = (user_id, note_id)

    return send_query(query, query_values)

def clear_note_labels_from_db(user_id: int, note_id: int) -> bool:

    query = """
        DELETE FROM "Note_assigned_labels"
        WHERE user_id = %s AND note_id = %s
    """
    query_values = (user_id, note_id)
    
    return send_query(query, query_values)
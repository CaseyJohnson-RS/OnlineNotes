

from .main import send_query, send_fetch_query
from common.schemas import User, Note, NoteShort

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


def get_note_from_db(user_id: int, note_id: int) -> Note | None:

    query = """SELECT * FROM "Notes" WHERE user_id = %s AND note_id = %s"""
    query_value = (user_id, note_id)

    note_data = send_fetch_query(query, query_value, 'one')
    note_status = convert_note_status(note_data["status"])

    if note_data is None: 
        return None
    
    note = Note(
        note_id=note_id,
        header=note_data["header"],
        text = note_data["text"],
        hex_color = note_data["hex_color"],
        status = note_status
    )

    return note


def get_note_labels(user_id: int, note_id: int) -> list[str]:

    query = """SELECT * FROM "Note_assigned_labels" WHERE user_id = %s AND note_id = %s"""
    query_value = (user_id, note_id)

    data_list = send_fetch_query(query, query_value, 'all')

    if data_list is None:
        return []

    label_list = []

    for row in data_list:
        label_list.append(row["label"])
    
    return label_list


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


def get_note_shorts_by_filter(
        user_id: int, 
        label: str | None = None,
        status: str | None = None
    ) -> list[NoteShort] | None:

    query = ""
    query_values = [user_id]

    if not label is None:
        query = """
            SELECT n.note_id, n.header, n.hex_color FROM "Note_assigned_labels" l 
                LEFT JOIN "Notes" n ON n.user_id = l.user_id AND n.note_id = l.note_id
                LEFT JOIN "Note_status" s ON n.status = s.id
                WHERE n.user_id = %s AND l.label = %s"""
        query_values.append(label)
    else:
        query = """
            SELECT n.note_id, n.header, n.hex_color FROM "Notes" n 
                LEFT JOIN "Note_status" s ON n.status = s.id
                WHERE n.user_id = %s"""     
    
    if not status is None:
        query += " AND s.title = %s"
        query_values.append(status)

    notes_data = send_fetch_query(query, tuple(query_values), fetch_type='all')
 
    if notes_data is None:
        return None
    
    notes = []

    for note_data in notes_data:

        print(note_data)

        note = NoteShort(
            note_id=note_data["note_id"],
            header=note_data["header"],
            hex_color = note_data["hex_color"],
        )

        notes.append(note)
    
    return notes


def set_label_to_note_in_db(user_id: int, note_id: int, label: str) -> bool:

    query = """
        INSERT INTO "Note_assigned_labels" (user_id, note_id, label)
        VALUES (%s,%s,%s)
    """
    query_values = (user_id, note_id, label)

    return send_query(query, query_values)


def unset_label_to_note_in_db(user_id: int, note_id: int, label: str) -> bool:

    query = """
        DELETE FROM "Note_assigned_labels"
        WHERE user_id = %s AND note_id = %s AND label = %s
    """
    query_values = (user_id, note_id, label)

    return send_query(query, query_values)


def create_user_label_db(user_id: int, label: str) -> bool:

    query = """
        INSERT INTO "User_note_labels" (user_id, label)
        VALUES (%s, %s);
    """
    query_values = (user_id, label)

    return send_query(query, query_values)


def delete_user_label_db(user_id: int, label: str) -> bool:

    query_clear_notes_labels = """
        DELETE FROM "Note_assigned_labels"
        WHERE user_id = %s AND label = %s
    """

    query_delete_label = """
        DELETE FROM "User_note_labels"
        WHERE user_id = %s AND label = %s
    """
    query_values = (user_id, label)

    return send_query(query_clear_notes_labels, query_values) and send_query(query_delete_label, query_values)


def get_all_user_labels(user_id: int) -> list[str]:

    query = """
        SELECT * FROM "User_note_labels"
        WHERE user_id = %s;
    """
    query_values = (user_id,)

    data_list = send_fetch_query(query, query_values, 'all')

    if data_list is None:
        return []

    label_list = [row["label"] for row in data_list]

    return label_list

# - - - - - - - - - - - - Profile API  - - - - - - - - - - - -

def update_user(
        user_id: int, 
        email: str | None = None,
        nickname: str | None = None,
        password_hash: str | None = None,
        active: bool | None = None,
        role_name: str | None = None
) -> bool:

    query = """UPDATE "Users" SET """
    query_values = []

    comma_check = False

    if not email is None:
        comma_check = True
        query += "email = %s "
        query_values.append(email)

        subquery_values = (email,)

        subquery = """UPDATE "Error_messages" SET email = %s WHERE email = %s;"""
        if not send_query(subquery, subquery_values):
            return False
    
        subquery = """UPDATE "Reviews" SET email = %s WHERE email = %s;"""
        if not send_query(subquery, subquery_values):
            return False
    
    if not nickname is None:
        query += (',' if comma_check else '') + "nickname = %s "
        query_values.append(nickname)
    
    if not password_hash is None:
        query += (',' if comma_check else '') + "password_hash = %s "
        query_values.append(password_hash)
    
    if not active is None:
        query += (',' if comma_check else '') + "active = %s "
        query_values.append(active)
    
    if not role_name is None:
        query += (',' if comma_check else '') + "role = %s "
        query_values.append(convert_role(role_name))
    
    query += " WHERE id=%s;"
    query_values.append(user_id)

    return send_query(query, query_values)


def delete_all_user_labels(user_id: int) -> bool:

    query = """
        DELETE FROM "User_note_labels"
        WHERE user_id = %s;
    """
    query_values = (user_id,)

    return send_query(query, query_values)


def clear_labels_from_all_notes(user_id: int) -> bool:

    query = """
        DELETE FROM "Note_assigned_labels"
        WHERE user_id = %s;
    """
    query_values = (user_id,)

    return send_query(query, query_values)


def deleta_all_user_notes(user_id: int) -> bool:

    query = """
        DELETE FROM "Notes"
        WHERE user_id = %s;
    """
    query_values = (user_id,)

    return send_query(query, query_values)


def delete_user(user_id: int) -> bool:

    query = """
        DELETE FROM "Users"
        WHERE id = %s;
    """
    query_values = (user_id,)

    return send_query(query, query_values)


def add_bug_report(email: str, text: str) -> bool:

    query = """
        INSERT INTO "Error_messages" (email, text)
        VALUES (%s, %s);
    """
    query_values = (email, text)

    return send_query(query, query_values)


def add_review(email: str, rating: int, text: str) -> bool:

    query = """
        INSERT INTO "Reviews" (email, rating, text)
        VALUES (%s, %s, %s);
    """
    query_values = (email, rating, text)

    return send_query(query, query_values)
from .main import conn


def DBSession(func):
    
    def wrapper(*args, **kwargs):
        cursor = conn.cursor()
        result = func(*args, **kwargs,cursor=cursor)
        cursor.close()
        return result
    
    return wrapper

@DBSession
def p(cursor):

    cursor.execute("SELECT * FROM \"Roles\"")

    res = cursor.fetchall()

    print(res)

p()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Этот код абсолютный кал

from common.schemas import User


fake_db = {
    "a@a.a" : {
        "id": 1,
        "nickname": "Casey",
        "password_hash": "$2b$12$j4zr9aO5JzjL1092w8q43O.kumInWxRb4ZML3ovjZMwzuIVqtV7Ey", # "cool"
        "active": True ,
        "role": "user"
    },

    "b@b.b" : {
        "id": 2,
        "nickname": "John",
        "password_hash": "$2b$12$ZszQjGzrpNr5tFhPlBP.lOJGcd8wmoFKXleI0Q8xFjwAJ0MrAfkiC", # "bed"
        "active": True ,
        "role": "user"
    },

    "c@c.c" : {
        "id": 3,
        "nickname": "John",
        "password_hash": "$2b$12$ZszQjGzrpNr5tFhPlBP.lOJGcd8wmoFKXleI0Q8xFjwAJ0MrAfkiC", # "bed"
        "active": True ,
        "role": "admin"
    }

}


def get_hashed_password_by_username(username: str) -> str | None:

    if username in fake_db:
        return fake_db[username]["password_hash"]

    return None


def get_user_id_by_username(username: str) -> int | None:

    if username in fake_db:
        return fake_db[username]["id"]

    return None


def get_user_by_id(user_id: int) -> User:

    email = ""

    for i in fake_db:
        if fake_db[i]["id"] == user_id:
            email = i
    
    user = User(email=email,**fake_db[email])

    return user


def add_user(username: str, password_hash: str, nickname: str, active: bool, role: str) -> bool:

    max_index = 1

    for i in fake_db:
        max_index = max_index < fake_db[i]["id"] and fake_db[i]["id"] or max_index

    fake_db[username] = {
        "password_hash": password_hash,
        "nickname": nickname,
        "active": active,
        "role": role,
        "id": max_index + 1
    }

    return max_index + 1
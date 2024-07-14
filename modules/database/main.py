from common.schemas import User


fake_db = {
    "a@a.com" : {
        "id": 1,
        "nickname": "Casey",
        "password_hash": "$2b$12$j4zr9aO5JzjL1092w8q43O.kumInWxRb4ZML3ovjZMwzuIVqtV7Ey", # "cool"
        "active": True ,
        "role": "user"
    },

    "b@b.com" : {
        "id": 2,
        "nickname": "John",
        "password_hash": "$2b$12$ZszQjGzrpNr5tFhPlBP.lOJGcd8wmoFKXleI0Q8xFjwAJ0MrAfkiC", # "bed"
        "active": True ,
        "role": "user"
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
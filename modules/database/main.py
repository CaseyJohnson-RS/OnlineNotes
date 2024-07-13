from common.schemas import User


fake_db = {
    "a@a.com" : {
        "id": 0,
        "nickname": "Casey",
        "password_hash": "c34045c1a1db8d1b3fca8a692198466952daae07eaf6104b4c87ed3b55b6af1b", # "cool"
        "active": False ,
        "role": "user"
    },

    "b@b.com" : {
        "id": 1,
        "nickname": "John",
        "password_hash": "c5052532c2206140dfdc3b0d756cce0831ac00fd978f2bfd150858e7ee217a8c", # "bed"
        "active": False ,
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
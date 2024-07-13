from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext

from ..database.main import get_hashed_password_by_username, get_user_id_by_username
from .config import ALGORITHM
from .constants import SECRET_KEY


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Получить хеш пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Функция хеширует пароль и сравнивает хеши 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Возвращает id пользователя или None
def authenticate_user(username: str, password: str) -> int | None:
    
    # Получение хеша пароля пользователя
    hashed_password = get_hashed_password_by_username(username)

    # Если пользователя в базе не было, то верхний уровень вернет ошибку
    if not hashed_password:
        return None

    access = verify_password(password, hashed_password)

    # Если пароль не совпадает, то верхний уровень вернет ошибку
    if not access:
        return None

    # Возвращаем id пользователя
    return get_user_id_by_username(username)


def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
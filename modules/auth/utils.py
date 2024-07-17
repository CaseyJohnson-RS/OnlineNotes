from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext
from random import seed, choices
import smtplib
from email.message import EmailMessage
import ssl

from ..database.crud import get_user_password_hash, get_user_id, add_user
from .config import ALGORITHM, EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD
from .constants import SECRET_KEY


# Инициализируем генератор случайных чисел
seed(datetime.now().microsecond)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Получить хеш пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Функция хеширует пароль и сравнивает хеши (нет, это не просто сравнение по буковкам)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Возвращает id пользователя или None
def authenticate_user(username: str, password: str) -> int | None:
    
    # Получение хеша пароля пользователя
    hashed_password = get_user_password_hash(username)

    # Если пользователя в базе не было, то верхний уровень вернет ошибку
    if not hashed_password:
        return None

    access = verify_password(password, hashed_password)

    # Если пароль не совпадает, то верхний уровень вернет ошибку
    if not access:
        return None

    # Возвращаем id пользователя
    return get_user_id(username)


# Создание токена доступа (чтобы не пришлось каждый раз вводить логин и пароль)
def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


# Функция для генерации последовательности чисел
def get_number_sequence(length: int) -> str:
    
    if length <= 0: 
        return ""

    return ''.join(choices([str(i) for i in range(0,10)], k=length))


# Проверка: находится ли логин в базе данных
def check_username_already_exists(username: str) -> bool:
    if get_user_id(username):
        return True
    return False


# Очевидно, создание пользоваталеля
# К слову, роль админа может дать никто. Да, её можно получить только 
# Если залесть в базу данных и поменять её вручную
# Надо как-то решать этот вопрос 
def create_user(username: str, password_hash: str, nickname: str) -> int:
    return add_user(username, password_hash, nickname, active=True, role="user")


# Отправка на почту кода подтверждения
def send_sequence_to_email(sequence:str, email: str) -> bool:

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD)

    msg = EmailMessage()
    
    msg['Subject'] = "Online Notes Confirm Code"
    msg['From'] = EMAIL_SENDER_ADDRESS
    msg['To'] = email
    msg.set_content(
f""" 
Hello! Thank you joining us!

Your confirm code: 
{sequence}
""")
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER_ADDRESS,EMAIL_SENDER_PASSWORD)
        smtp.sendmail(EMAIL_SENDER_ADDRESS, email, msg.as_string())

    return True
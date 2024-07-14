from typing import Annotated
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr

from .utils import check_username_already_exists, \
    get_password_hash, \
    get_number_sequence, \
    send_sequence_to_email, \
    create_user, \
    create_access_token
from .exceptions import USERNAME_EXISTS_EXCEPTION, \
    LATE_CONFIRM_EXCEPTION, \
    BAD_CONFIRMATION_EXCEPTION, \
    WRONG_CONFIRMATION_EXCEPTION
from .config import CONFIRMATION_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import Token
from modules.logging.main import Log

from fastapi import APIRouter, BackgroundTasks, Query, Form

router = APIRouter()


# Будет использоваться для подтверждения почты
# Рассчет на то, что одновременно регистрироваться будут не тысячи человек
# Иначе пришлось бы использовать что-то другое
# Сюда будут записываться данные пользователя с кодом подтверждения
# До того, пока не произойдет подтверждение регистрации
# ! Не понятно как правильно очищать !
sign_up_buffer = { }


# Вспомогательная функция для фронта
# Чтобы заранее чекать, есть ли пользователь с подобным логином
@router.post("/username-exist")
def check_username_exist(
        username: Annotated[EmailStr, Query(
            title="Логин",
            description="Адрес электронной почты, который используется как логин"
        )]
    ) -> bool:
    """
    Проверяет, есть ли в базе данный логин
    - <mark>True</mark> - в базе есть такой логин
    - <mark>False</mark> - в базе нет такого логина
    """
    return check_username_already_exists(username)


# Регистрация с последующим подтверждением почты (см. /sign-up-confirm)
@router.post("/sign-up")
def sign_up(
        username: Annotated[EmailStr, Form(
            title="Логин",
            description="Адрес электронной почты, который используется как логин"
        )],
        password: Annotated[str, Form(
            title="Пароль", 
            min_length=8, 
            max_length=32
        )],
        nickname: Annotated[str, Form(
            title="Имя, ник, псевдоним, называй как хочешь",
            max_length=64
        )],
        backgroun_tasks: BackgroundTasks # Это класс, чтобы не ждать ответа, заставляет код выполнятся на фоне
    ) -> bool:
    """
    Проверяет, есть ли данный логин (электронная почта) в базе данных
    и возвращает ошибку, если есть. Хеширует пароль и добавляет 
    пользователя в буфер, до последующего подтверждения в течение определенного количества
    минут. Подтверждение происходит по коду, который приходит на почту.
    Этот код нужно отправить вместе с логином на путь '/registration_confirm'
    """

    Log("# Registration request")
    Log(f"Username: {username}")
    Log(f"Password: {password}")
    Log(f"Nickname: {nickname}")

    if check_username_already_exists(username):
        Log("Username already exists. Denied")
        raise USERNAME_EXISTS_EXCEPTION
    
    hashed_password = get_password_hash(password)
    confirm_sequence = get_number_sequence(6)

    Log(f"Send confirm sequence: " + confirm_sequence)

    backgroun_tasks.add_task(send_sequence_to_email, confirm_sequence, username)

    sign_up_buffer[username] = {
        "nickname": nickname,
        "password_hash": hashed_password,
        "confirm_sequence": confirm_sequence,
        "confirm_expires": datetime.now(timezone.utc) + timedelta(minutes=CONFIRMATION_EXPIRE_MINUTES)
    }

    Log(f"Waiting for confirmation within {CONFIRMATION_EXPIRE_MINUTES} minutes...")

    return True


# Подтверждение регистрации
@router.post("/sign-up-confirm")
def sign_up_confirm(
        username: Annotated[EmailStr, Form(
            title="Логин",
            description="Адрес электронной почты, который используется как логин"
        )],
        confirm_seq: Annotated[str, Form(
            description="Код, который пришел на почтовый ящик"
        )]
    ) -> Token:
    """
    Проверяет:
    - Был ли пользователь в буфере регистрации?
    - Не прошло ли доступное время подтверждения? 
    - Совпадает ли сгенерированный код с тем, что ввёл пользователь?

    Если всё впорядке, то создает пользователя и возвращает токен доступа
    """

    Log("# Redistration confirm request")

    # Был ли пользователь в буфере регистрации?
    if not username in sign_up_buffer:
        Log("User name wasn't in the buffer of confirmation. Denied")
        raise BAD_CONFIRMATION_EXCEPTION
    
    # Не прошло ли доступное время подтверждения? 
    if sign_up_buffer[username]["confirm_expires"] < datetime.now(timezone.utc):
        Log("Late confirmation. Denied")
        del sign_up_buffer[username]
        raise LATE_CONFIRM_EXCEPTION
    
    # Совпадает ли сгенерированный код с тем, что ввёл пользователь?
    if confirm_seq != sign_up_buffer[username]["confirm_sequence"]:
        Log(f"Wrong confirm sequence {confirm_seq}. Expected " + sign_up_buffer[username]["confirm_sequence"] + ". Denied")
        del sign_up_buffer[username]
        raise WRONG_CONFIRMATION_EXCEPTION
    
    # Создаем пользователя
    user_id = create_user(username, sign_up_buffer[username]["password_hash"], sign_up_buffer[username]["nickname"])

    Log(f"User created (id = {user_id})")

    # Создаем токен доступа
    assecc_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_id}, expires_delta=assecc_token_expires)

    Log(f"Token created with params: data(user_id={user_id}) token_expires({ACCESS_TOKEN_EXPIRE_MINUTES})")

    return Token(access_token=access_token, token_type="bearer")
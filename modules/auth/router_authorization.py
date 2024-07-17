from typing import Annotated
from datetime import timedelta

from .schemas import Token
from .utils import authenticate_user, create_access_token
from .exceptions import UNAUTHORIZED_EXCEPTION
from .config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..logging.main import Log

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

# Создаем маршрутизатор для подключения его к основному приложению
router = APIRouter()

# Авторизация
@router.post("/token", tags=["Authorization"])
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:

    """
    Принимает логин и пароль и возвращает токен доступа. 
    Естественно возвращает ошибку, если логин и пароль были недействительными
    """

    Log(f"Authorization: request access token")
    Log(f"Username: {form_data.username}")
    Log(f"Password: {form_data.password}")

    # Аутентифицируем пользователя
    user_id = authenticate_user(form_data.username, form_data.password)

    Log(f"User id: {user_id}")

    # Если что-то пошло не так, то вызываем ошибку
    if user_id is None:
        Log(f"Access denied")
        raise UNAUTHORIZED_EXCEPTION
    
    # Иначе начинаем создавать токен доступа
    # Фиксируем время сгорания токена
    assecc_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_id}, expires_delta=assecc_token_expires)

    Log(f"Token created with params: data(user_id={user_id}) token_expires({ACCESS_TOKEN_EXPIRE_MINUTES})")

    return Token(access_token=access_token, token_type="bearer")
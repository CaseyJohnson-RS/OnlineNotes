from typing import Annotated
from datetime import timedelta

from .schemas import Token
from .utils import authenticate_user, create_access_token
from .exceptions import UNAUTHORIZED_EXCEPTION
from .config import ACCESS_TOKEN_EXPIRE_MINUTES

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

# Создаем маршрутизатор для подключения его к основному приложению
router = APIRouter()


@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:

    # Аутентифицируем пользователя
    user_id = authenticate_user(form_data.username, form_data.password)

    # Если что-то пошло не так, то вызываем ошибку
    if not user_id:
        raise UNAUTHORIZED_EXCEPTION
    
    # Иначе начинаем создавать токен доступа
    # Фиксируем время сгорания токена
    assecc_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Создаем токен
    access_token = create_access_token(data={"sub": user_id}, timedelta=assecc_token_expires)

    return Token(access_token=access_token, token_type="bearer")

# Допиши регистрацию
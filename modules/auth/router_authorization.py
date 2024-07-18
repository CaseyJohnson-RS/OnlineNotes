from typing import Annotated

from .schemas import Token
from .utils import authenticate_user, create_access_token
from .exceptions import UNAUTHORIZED_EXCEPTION
from ..logging.main import Log, LogTime

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

# Создаем маршрутизатор для подключения его к основному приложению
router = APIRouter()

# Авторизация
@router.post("/token", tags=["Token"])
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:

    """
    Принимает логин и пароль и возвращает токен доступа. 
    Естественно возвращает ошибку, если логин и пароль были недействительными
    """

    LogTime()
    Log(
        f"Authorization: request access token\n" +
        f"Username: {form_data.username}\n" + 
        f"Password: {form_data.password}"
    )

    user_id = authenticate_user(form_data.username, form_data.password)

    if user_id is None:
        Log("Access denied")
        raise UNAUTHORIZED_EXCEPTION
    
    access_token = create_access_token(data={"sub": user_id})

    Log(f"Token created with params (user_id={user_id})")

    return Token(access_token=access_token, token_type="bearer")
from typing import Annotated

from common.schemas import User 
from .exceptions import CREDENTIALS_EXCEPTION, INACTIVE_USER_EXCEPTION
from .config import ALGORITHM
from .constants import SECRET_KEY
from ..database.main import get_user_by_id
from ..logging.main import Log

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import jwt
from jwt.exceptions import InvalidTokenError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Похоже, что при отсутствии токена OAuth2 сам прерывает
# Выполнение функции и вызывает ошибку, которую нельзя отследить
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")

        if user_id is None:

            Log("Such a user doesn't exist. Access denied")
            
            raise CREDENTIALS_EXCEPTION
        
    except InvalidTokenError:

        Log("Invalin Token. Access denied")

        raise CREDENTIALS_EXCEPTION
    
    user = get_user_by_id(user_id)
    
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:

    if not current_user.active:

        Log("User is inactive. Access denied")

        raise INACTIVE_USER_EXCEPTION
 
    return current_user
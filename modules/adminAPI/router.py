from typing import Annotated
from common.schemas import User, Error_message, Review
from pydantic import EmailStr

from modules.auth.dependences import get_current_active_user
from modules.database.crud import get_user, update_user, delete_all_user_labels, clear_labels_from_all_notes, deleta_all_user_notes, delete_user, get_error_messages, get_reviews
from modules.auth.utils import get_password_hash

from .exceptions import INSUFFICIENT_PERMISSIONS_EXCEPTION, RIGTHS_CONFLICT_EXCEPTION

from fastapi import APIRouter, Depends, Body, Query

# Создаем маршрутизатор для подключения его к основному приложению
router = APIRouter()


def verify_admin(user: Annotated[User, Depends(get_current_active_user)]) -> User:

    if user.role != "admin":
        raise INSUFFICIENT_PERMISSIONS_EXCEPTION
    
    return user

@router.get("/admin-get-user", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def get_user_info_by_email(email: Annotated[EmailStr, Query()]) -> User | None: 
    return get_user(email)


@router.patch("/admin-set-user-active", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def set_user_active(user_id: Annotated[int, Body()], active: Annotated[bool, Body()]) -> bool:

    user = get_user(user_id)

    if user.role == "admin":
        raise RIGTHS_CONFLICT_EXCEPTION

    return update_user(user_id=user_id, active=active)


@router.patch("/admin-delete-user", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def delete_user_account(user_id: Annotated[int, Body()]) -> bool:

    user = get_user(user_id)

    if user.role == "admin":
        raise RIGTHS_CONFLICT_EXCEPTION

    return delete_all_user_labels(user.id) and \
        clear_labels_from_all_notes(user.id) and \
        deleta_all_user_notes(user.id) and \
        delete_user(user.id)


@router.patch("/admin-set-user-email", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def set_user_email(user_id: Annotated[int, Body()], email: Annotated[EmailStr, Body()]) -> bool:

    user = get_user(user_id)

    if user.role == "admin":
        raise RIGTHS_CONFLICT_EXCEPTION

    return update_user(user_id = user_id, email=email)


@router.patch("/admin-set-user-password", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def set_user_password(user_id: Annotated[int, Body()], password: Annotated[str, Body()]) -> bool:

    user = get_user(user_id)

    if user.role == "admin":
        raise RIGTHS_CONFLICT_EXCEPTION
    
    password_hash = get_password_hash(password)

    return update_user(user_id = user_id, password_hash=password_hash)


@router.get("/admin-get-error-messages", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def read_error_messages(offset: Annotated[int, Query()] = 0, limit: Annotated[int, Query()] = 10) -> list[Error_message]:
    return get_error_messages(offset, limit)


@router.get("/admin-get-reviews", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def read_reviews(offset: Annotated[int, Query()] = 0, limit: Annotated[int, Query()] = 10) -> list[Review]:
    return get_reviews(offset, limit)


@router.patch("/admin-set-user-nickname", dependencies=[Depends(verify_admin)], tags=["AdminAPI"])
def set_nickname(user_id: Annotated[int, Body()], nickname: Annotated[str, Body()]) -> bool:
    return update_user(user_id, nickname=nickname)
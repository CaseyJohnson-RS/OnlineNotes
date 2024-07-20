from typing import Annotated

from common.schemas import User

from modules.auth.dependences import get_current_active_user
from modules.database.crud import update_user, delete_all_user_labels, clear_labels_from_all_notes, deleta_all_user_notes, delete_user, add_bug_report, add_review

from fastapi import APIRouter, Depends, Body, Query

# Создаем маршрутизатор для подключения его к основному приложению
router = APIRouter()


@router.post("/set-nickname", tags=["ProfileAPI"])
def set_nickname(user: Annotated[User, Depends(get_current_active_user)], nickname: Annotated[str, Query()]) -> bool:
    return update_user(user.id, nickname=nickname)


@router.delete("/delete-account", tags=["ProfileAPI"])
def delete_account(user: Annotated[User, Depends(get_current_active_user)]) -> bool:     
    return delete_all_user_labels(user.id) and \
        clear_labels_from_all_notes(user.id) and \
        deleta_all_user_notes(user.id) and \
        delete_user(user.id)


@router.post("/bug-report", tags=["ProfileAPI"])
def post_bug_report(
    user: Annotated[User, Depends(get_current_active_user)],
    text: Annotated[str, Body()]
) -> bool:
    return add_bug_report(user.email, text);


@router.post("/leave-review", tags=["ProfileAPI"])
def post_review(
    user: Annotated[User, Depends(get_current_active_user)],
    rating: Annotated[int, Body()],
    text: Annotated[str, Body()]
) -> bool:
    return add_review(user.email, rating, text);


@router.get("/profile-info", tags=["ProfileAPI"])
def get_profile_information(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return user;
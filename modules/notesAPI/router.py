from typing import Annotated
from common.schemas import User, Note

from modules.auth.dependences import get_current_active_user
from modules.database.crud import create_note_in_db, update_note_in_db, delete_note_in_db, clear_note_labels_from_db

from fastapi import APIRouter, Depends, Body

# Создаем маршрутизатор для подключения его к основному приложению
router = APIRouter()


@router.post("/create-note", tags=["NotesAPI"])
def create_note(user: Annotated[User, Depends(get_current_active_user)]):
    return create_note_in_db(user_id=user.id)


@router.patch("/update-note", tags=["NotesAPI"])
def update_note(user: Annotated[User, Depends(get_current_active_user)], note: Annotated[Note, Body()]) -> bool:
    return update_note_in_db(user_id=user.id, note=note)

@router.delete("/delete-note", tags=["NotesAPI"])
def delete_note(user: Annotated[User, Depends(get_current_active_user)], note_id: Annotated[int, Body()]) -> bool:
    if clear_note_labels_from_db(user.id, note_id):
        return delete_note_in_db(user.id, note_id)
    else:
        return False


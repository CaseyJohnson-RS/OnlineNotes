from typing import Annotated
from common.schemas import User, Note, NoteLabeled

from modules.auth.dependences import get_current_active_user
from modules.database.crud import create_note_in_db, \
    update_note_in_db, \
    delete_note_in_db, \
    clear_note_labels_from_db, \
    get_note_shorts_by_filter, \
    get_note_labels, \
    get_note_from_db, \
    set_label_to_note_in_db, \
    unset_label_to_note_in_db, \
    create_user_label_db, \
    delete_user_label_db, \
    get_all_user_labels

from fastapi import APIRouter, Depends, Body, Query

# Создаем маршрутизатор для подключения его к основному приложению
router = APIRouter()


@router.get("/get-note", tags=["NotesAPI"])
def get_note(user: Annotated[User, Depends(get_current_active_user)], note_id: Annotated[int, Query()]) -> NoteLabeled | None:
    
    note = get_note_from_db(user.id, note_id)

    if note is None:
        return None

    labels = get_note_labels(user.id, note_id)

    labeled_note = NoteLabeled(
        note_id=note.note_id,
        header=note.header,
        hex_color=note.hex_color,
        text=note.text,
        status=note.status,
        labels=labels
    )

    return labeled_note


# Получить заметки по ярлыку
@router.get("/get-notes", tags=["NotesAPI"])
def get_notes(
    user: Annotated[User, Depends(get_current_active_user)], 
    label: Annotated[str, Query()] = None
) -> list[Note] | None:
    return get_note_shorts_by_filter(user_id=user.id, label=label, status='active')


@router.get("/get-notes-archived", tags=["NotesAPI"])
def get_noted_archived(user: Annotated[User, Depends(get_current_active_user)]) -> list[Note] | None:
    return get_note_shorts_by_filter(user_id=user.id, status='archived')


@router.get("/get-notes-deleted", tags=["NotesAPI"])
def get_noted_deleted(user: Annotated[User, Depends(get_current_active_user)]) -> list[Note] | None:
    return get_note_shorts_by_filter(user_id=user.id, status='deleted')


# Создать заметку
@router.post("/create-note", tags=["NotesAPI"])
def create_note(user: Annotated[User, Depends(get_current_active_user)]) -> int:
    return create_note_in_db(user_id=user.id)

# Архивировать / разархивировать
# Удалить / восстановить
# Изменить цвет
# Изменить текст и заголовок
@router.patch("/update-note", tags=["NotesAPI"])
def update_note(user: Annotated[User, Depends(get_current_active_user)], note: Annotated[Note, Body()]) -> bool:
    return update_note_in_db(user_id=user.id, note=note)


# Удалить заметку польностью
@router.delete("/delete-note", tags=["NotesAPI"])
def delete_note(user: Annotated[User, Depends(get_current_active_user)], note_id: Annotated[int, Body()]) -> bool:
    if clear_note_labels_from_db(user.id, note_id):
        return delete_note_in_db(user.id, note_id)
    else:
        return False


@router.post("/set-label", tags=["NotesAPI"])
def set_label_to_note(
    user: Annotated[User, Depends(get_current_active_user)], 
    note_id: Annotated[int, Query()],
    label: Annotated[str, Query()]
) -> bool:
    return set_label_to_note_in_db(user.id, note_id, label)


@router.post("/unset-label", tags=["NotesAPI"])
def unset_label_from_note(
    user: Annotated[User, Depends(get_current_active_user)], 
    note_id: Annotated[int, Query()],
    label: Annotated[str, Query()]
) -> bool:
    return unset_label_to_note_in_db(user.id, note_id, label)


@router.post("/create-label", tags=["NotesAPI"])
def create_user_label(
    user: Annotated[User, Depends(get_current_active_user)], 
    label: Annotated[str, Query()]
) -> bool:
    return create_user_label_db(user.id, label)


@router.delete("/delete-label", tags=["NotesAPI"])
def create_user_label(
    user: Annotated[User, Depends(get_current_active_user)], 
    label: Annotated[str, Query()]
) -> bool:
    return delete_user_label_db(user.id, label)


@router.get("/get-user-labels", tags=["NotesAPI"])
def get_user_labels(
    user: Annotated[User, Depends(get_current_active_user)]
) -> list[str]:
    return get_all_user_labels(user.id)


@router.post("/clear-note-labels", tags=["NotesAPI"])
def clear_note_labels(
    user: Annotated[User, Depends(get_current_active_user)],
    note_id: Annotated[int, Query()],
) -> bool:
    
    return clear_note_labels_from_db(user.id, note_id)
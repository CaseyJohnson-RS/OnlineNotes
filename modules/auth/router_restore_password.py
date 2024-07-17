from typing import Annotated
from datetime import datetime, timedelta, timezone

from .utils import check_username_already_exists, send_sequence_to_email, get_number_sequence, get_password_hash, create_access_token
from .exceptions import BAD_CONFIRMATION_EXCEPTION, LATE_CONFIRM_EXCEPTION, WRONG_CONFIRMATION_EXCEPTION, BAD_PASS_RESTORE_EXCEPTION, LATE_RESTORE_EXCEPTION
from .config import RESTORE_CONFIRM_EXPIRE_MINUTES, NEW_PASSWORD_WAIT_EXPIRE_MINUTES
from .schemas import Token

from modules.logging.main import Log, LogTime
from modules.database.crud import update_password_hash, get_user_id

from fastapi import APIRouter, Form, BackgroundTasks


router = APIRouter()


restore_confirm_buffer = {}
set_new_password_buffer = {}


@router.post("/restore-password", tags=["Authorization", "Restore password"])
def restore_password_by_username(
    username: Annotated[str, Form()],
    bgtasks: BackgroundTasks
) -> bool:
    
    LogTime()
    Log("Restore password request")
    
    if not check_username_already_exists(username=username):
        Log(f"User name {username} doesn't exist. Denied")
        return False
    
    confirm_sequence = get_number_sequence(6)
    
    bgtasks.add_task(send_sequence_to_email, confirm_sequence, username)

    Log(f"Send confirm password restore sequence {confirm_sequence}")

    restore_confirm_buffer[username] = {
        "confirm_sequence": confirm_sequence,
        "confirm_expires": datetime.now(timezone.utc) + timedelta(minutes=RESTORE_CONFIRM_EXPIRE_MINUTES)
    }

    Log(f"Wating for confirm password restore from {username} within {RESTORE_CONFIRM_EXPIRE_MINUTES} minutes...")

    return True


@router.post("/restore-password-confirm", tags=["Authorization", "Restore password"])
def confirm_password_restore(
    username: Annotated[str, Form()],
    confirm_seq: Annotated[str, Form(
            description="Код, который пришел на почтовый ящик"
        )]
) -> bool:
    
    LogTime()
    Log("Confirm password restore request")
    
    # Был ли пользователь в буфере восстановления пароля?
    if not username in restore_confirm_buffer:
        Log("User name wasn't in the buffer of restore confirmation. Denied")
        raise BAD_CONFIRMATION_EXCEPTION
    
    # Не прошло ли доступное время подтверждения? 
    if restore_confirm_buffer[username]["confirm_expires"] < datetime.now(timezone.utc):
        Log("Late restore confirmation. Denied")
        del restore_confirm_buffer[username]
        raise LATE_CONFIRM_EXCEPTION
    
    # Совпадает ли сгенерированный код с тем, что ввёл пользователь?
    if confirm_seq != restore_confirm_buffer[username]["confirm_sequence"]:
        Log(f"Wrong confirm sequence {confirm_seq}. Expected " + restore_confirm_buffer[username]["confirm_sequence"] + ". Denied")
        del restore_confirm_buffer[username]
        raise WRONG_CONFIRMATION_EXCEPTION
    
    del restore_confirm_buffer[username]
    
    set_new_password_buffer[username] = {
        "wait_password_expires": datetime.now(timezone.utc) + timedelta(minutes=NEW_PASSWORD_WAIT_EXPIRE_MINUTES)
    }

    Log(f"Wating for password change from {username} within {NEW_PASSWORD_WAIT_EXPIRE_MINUTES} minutes...")

    return True


@router.post("/set-new-password", tags=["Authorization", "Restore password"])
def set_new_password_for_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
) -> Token:
    
    LogTime()
    Log("Set new password request")
    
    # Был ли пользователь в буфере восстановления пароля?
    if not username in set_new_password_buffer:
        Log("User name wasn't in the buffer of set password. Denied")
        raise BAD_PASS_RESTORE_EXCEPTION
    
    # Не прошло ли доступное время подтверждения? 
    if set_new_password_buffer[username]["wait_password_expires"] < datetime.now(timezone.utc):
        Log("Too late to restore password. Denied")
        del restore_confirm_buffer[username]
        raise LATE_RESTORE_EXCEPTION

    password_hash = get_password_hash(password=password)
    user_id = get_user_id(username)

    update_password_hash(username, password_hash=password_hash)

    Log("Password updated")

    access_token = create_access_token(data={"sub": user_id})

    Log(f"Token created with params (user_id={user_id})")

    del set_new_password_buffer[username]

    return Token(access_token=access_token, token_type="bearer")

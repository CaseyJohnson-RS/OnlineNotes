from typing import Annotated

from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: Annotated[int, Field()]
    email: Annotated[EmailStr, Field()]
    password_hash: Annotated[str, Field()]
    active: Annotated[bool, Field(default=True)]
    role: Annotated[str, Field()]


class NoteOut(BaseModel):
    note_id: Annotated[int, Field()]
    date_of_creation: Annotated[datetime, Field()]
    header: Annotated[str, Field()]
    text: Annotated[str, Field()]
    hex_color: Annotated[str, Field()]
    assigned_labels: Annotated[list[int], Field()]
    images: Annotated[list[str], Field()]
    status: Annotated[str, Field()]


class UserOut(BaseModel):
    id: Annotated[int, Field()]
    nickname: Annotated[str, Field()]  
    username: Annotated[EmailStr, Field()]
    avatar: Annotated[str, Field()]
    role: Annotated[str, Field()]
    active: Annotated[bool, Field(default=True)]
    labels: Annotated[list[str], Field()]
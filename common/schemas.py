from typing import Annotated

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: Annotated[int, Field()]
    email: Annotated[EmailStr, Field()]
    password_hash: Annotated[str, Field()]
    active: Annotated[bool, Field(default=True)]
    role: Annotated[str, Field()]


class NoteShort(BaseModel):
    note_id: int
    header: Annotated[str | None, Field()] = None
    hex_color: Annotated[str | None, Field()] = None


class Note(NoteShort):
    text: Annotated[str | None, Field()] = None
    status: Annotated[str | None, Field()] = None


class NoteLabeled(Note):
    labels: Annotated[list[str], Field()] = []
    
    
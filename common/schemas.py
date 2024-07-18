from typing import Annotated

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: Annotated[int, Field()]
    email: Annotated[EmailStr, Field()]
    nickname: Annotated[str | None, Field()] = None
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
    
    
class Error_message(BaseModel):
    id: int
    author_email: EmailStr
    text: str


class Review(BaseModel):
    id: int
    rating: int
    author_email: EmailStr
    text: str
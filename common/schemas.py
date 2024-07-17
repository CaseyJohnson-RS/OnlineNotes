from typing import Annotated

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: Annotated[int, Field()]
    email: Annotated[EmailStr, Field()]
    password_hash: Annotated[str, Field()]
    active: Annotated[bool, Field(default=True)]
    role: Annotated[str, Field()]


class Note(BaseModel):
    note_id: int
    header: Annotated[str | None, Field()]
    text: Annotated[str | None, Field()]
    hex_color: Annotated[str | None, Field()]
    status: Annotated[str | None, Field()]


class UserOut(BaseModel):
    id: Annotated[int, Field()]
    nickname: Annotated[str, Field()]  
    username: Annotated[EmailStr, Field()]
    avatar: Annotated[str, Field()]
    role: Annotated[str, Field()]
    active: Annotated[bool, Field(default=True)]
    labels: Annotated[list[str], Field()]
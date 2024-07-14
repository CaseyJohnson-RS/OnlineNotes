from typing import Annotated
from pydantic import BaseModel, Field

# Pydantic модель токена
class Token(BaseModel):
    access_token: str
    token_type: str
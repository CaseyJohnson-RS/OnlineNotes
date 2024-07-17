from pydantic import BaseModel

# Pydantic модель токена
class Token(BaseModel):
    access_token: str
    token_type: str
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def auth():
    return "Hello world!"
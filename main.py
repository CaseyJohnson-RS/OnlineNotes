from fastapi import FastAPI

app = FastAPI()

from modules.auth import router

app.include_router(router.router)
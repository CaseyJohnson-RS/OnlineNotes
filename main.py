from typing import Annotated

from modules.auth.dependences import get_current_active_user

from fastapi import FastAPI, Depends

app = FastAPI()
routers = []

from modules.auth import main

routers += main.routers

for router in routers:
    app.include_router(router=router)


from common.schemas import User

@app.get("/")
def main(user: Annotated[User, Depends(get_current_active_user)]):

    return "Hello!"
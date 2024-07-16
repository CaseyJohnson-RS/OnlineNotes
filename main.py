from contextlib import asynccontextmanager
from fastapi import FastAPI
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Тут твой код

from modules.auth import main as m_auth
from modules.logging import main as m_logging

def initialize(app: FastAPI):

    routers = []
    routers += m_auth.routers
    routers += m_logging.routers

    for router in routers:
        app.include_router(router)


def shutdown(app: FastAPI):

    m_auth.shutdown()
    m_logging.shutdown()
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
@asynccontextmanager
async def lifespan(app: FastAPI):

    initialize(app)

    yield

    shutdown(app)

app = FastAPI(lifespan=lifespan)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""
from typing import Annotated
from common.schemas import User
from fastapi import Depends
from modules.auth.dependences import get_current_active_user

@app.get("/")
def g(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return user"""
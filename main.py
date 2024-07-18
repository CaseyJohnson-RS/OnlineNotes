from contextlib import asynccontextmanager
from fastapi import FastAPI
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Тут твой код

from modules.auth import main as m_auth
from modules.logging import main as m_logging
from modules.notesAPI import main as m_notesAPI

def initialize(app: FastAPI):

    routers = []
    routers += m_auth.routers
    routers += m_logging.routers
    routers += m_notesAPI.routers

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
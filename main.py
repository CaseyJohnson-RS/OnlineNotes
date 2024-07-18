from contextlib import asynccontextmanager
from fastapi import FastAPI
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Тут твой код

from modules.logging import main as m_logging
from modules.auth import main as m_auth
from modules.notesAPI import main as m_notesAPI
from modules.profileAPI import main as m_profileAPI
from modules.adminAPI import main as m_adminAPI

def initialize(app: FastAPI):

    routers = []
    routers += m_auth.routers
    routers += m_logging.routers
    routers += m_notesAPI.routers
    routers += m_profileAPI.routers
    routers += m_adminAPI.routers

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
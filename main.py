from dotenv import load_dotenv; load_dotenv();
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

from modules import auth 
from modules import notesAPI 
from modules import profileAPI
from modules import adminAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

description = """
Writers' Favorite App 🖊️

This is the interface for the user part of the application.

Application features:

 - Authorization
 - Adding notes
 - Adding shortcuts to notes
 - Archiving
 - etc.
"""

title="Online Notes"
version="0.0.1"
contact={
    "name": "Casey Johnson",
    "email": "sharus.programmer@gmail.com",
}
license_info={
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

app = FastAPI(
    title=title,
    description=description,
    version=version,
    contact=contact,
    license_info=license_info,
    docs_url="/documentation", 
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = []
routers += auth.routers
routers += notesAPI.routers
routers += profileAPI.routers
routers += adminAPI.routers

for router in routers:
    app.include_router(router)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


@app.get("/hi", tags=["Fun"])
def return_hello():
    return "Hello"

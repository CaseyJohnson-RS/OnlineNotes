from typing import Annotated

from fastapi import FastAPI


app = FastAPI()

@app.get("/post")
async def read_items(a : int = 0, b : int = 0):
    return {"result": a + b}

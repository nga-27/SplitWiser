import os
import signal

import dotenv
from fastapi import FastAPI, Response

from api.routers import status, transactions
from api.libs.db import reset_db, init_db

app = FastAPI()

app.include_router(status.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/start")
async def start():
    from dotenv import load_dotenv
    DOTENV_PATH = os.path.join(os.getcwd(),'.env')
    load_dotenv(DOTENV_PATH)
    db_path = os.getenv("INPUT_SOURCE_PATH")
    init_db(db_path)

@app.get("/shutdown")
async def shutdown():
    # We'll want to save the DB at this point!
    reset_db()
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content="Server is shutting down...")

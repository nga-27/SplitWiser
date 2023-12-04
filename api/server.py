import os
import signal
import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Response

from api.routers import summary, transactions
from api.libs.db import reset_db, init_db, save_db, archive_db

app = FastAPI()

app.include_router(summary.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    message = "Hello from SplitWiser! The current time is " +\
        f"{datetime.datetime.now().strftime('%m/%d/%Y_%H:%M:%S.%f')}"
    return {"message": message}

@app.get("/start")
async def start():
    DOTENV_PATH = os.path.join(os.getcwd(),'.env')
    load_dotenv(DOTENV_PATH)
    db_path = os.getenv("INPUT_SOURCE_PATH")
    archive_db(db_path)
    init_db(db_path)
    summary.update_summary()

@app.get("/shutdown")
async def shutdown():
    # We'll want to save the DB at this point!
    DOTENV_PATH = os.path.join(os.getcwd(),'.env')
    load_dotenv(DOTENV_PATH)
    db_path = os.getenv("INPUT_SOURCE_PATH")
    save_db(db_path)
    reset_db()
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content="Server is shutting down...")

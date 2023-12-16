""" Primary FastAPI server for backend code """
import os
import signal
import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Response

from api.routers import summary, transactions, payments
from api.libs.db import reset_db, init_db, save_db, archive_db

DOTENV_PATH = os.path.join(os.getcwd(),'.env')
load_dotenv(DOTENV_PATH)

app = FastAPI()

app.include_router(summary.router)
app.include_router(transactions.router)
app.include_router(payments.router)

@app.get("/")
async def root():
    """ Basic 'hello world' with a current time to verify alertness """
    message = "Hello from SplitWiser! The current time is " +\
        f"{datetime.datetime.now().strftime('%m/%d/%Y_%H:%M:%S.%f')}"
    return {"message": message}


@app.get("/start")
async def start():
    """ Start the application by pulling in the DB as needed """
    db_path = os.getenv("INPUT_SOURCE_PATH")
    archive_db(db_path)
    init_db(db_path)
    summary.update_summary()
    return Response(status_code=200, content="DB and system are activated.")


@app.get("/shutdown")
async def shutdown():
    """ Save the DB back to the spreadsheet, and kill the API process """
    db_path = os.getenv("INPUT_SOURCE_PATH")
    summary.update_summary()
    save_db(db_path)
    reset_db()
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content="Server is shutting down...")

import os
import signal
from fastapi import FastAPI, Response

from api.routers import status, transactions

app = FastAPI()

app.include_router(status.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/shutdown")
async def shutdown():
    # We'll want to save the DB at this point!
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content="Server is shutting down...")

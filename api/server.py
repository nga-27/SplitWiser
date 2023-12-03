import os
import signal
from fastapi import FastAPI, Response

from api.routers.status import router as status_router

app = FastAPI()

app.include_router(status_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/shutdown")
async def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content="Server is shutting down...")
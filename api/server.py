from fastapi import FastAPI

from api.routers.status import router as status_router

app = FastAPI()

app.include_router(status_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.send import router as send_router

app = FastAPI(title="AI Email Assistant")

app.include_router(chat_router)
app.include_router(send_router)


@app.get("/")
def root():
    return {"status": "running"}
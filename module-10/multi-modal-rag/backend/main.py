from fastapi import FastAPI

from routes.chat import router as chat_router
from routes.upload import router as upload_router

app = FastAPI(
    title="Multi Modal RAG"
)

app.include_router(chat_router)
app.include_router(upload_router)


@app.get("/")
def health():

    return {
        "status": "healthy"
    }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.workflow import router as workflow_router

app = FastAPI(title="AI Software Engineering Assistant Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router, prefix="/ai", tags=["ai"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

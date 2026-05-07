from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.predictions import router as predictions_router
from app.core.config import get_settings
from app.core.logging import configure_logging, log_requests

settings = get_settings()
configure_logging()

app = FastAPI(
    title="TubePilot AI API",
    description="Backend API for the YouTube Creator Copilot MVP.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(predictions_router)
app.include_router(documents_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "TubePilot AI API",
        "environment": settings.app_env,
        "docs": "/docs",
    }

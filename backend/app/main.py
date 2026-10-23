from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.config import settings

from app.api.upload import(
    router as upload_router
)

from app.api.dashboard import(
    router as dashboard_router
)

from app.api.history import (
    router as history_router
)

from app.api.insights import(
    router as insights_router
)

from app.api.graph import (
    router as graph_router
)

from app.api.documents import (
    router as documents_router
)

from app.api.document_summary import (
    router as document_summary_router
)

from app.api.chat_history import (
    router as chat_history_router
)

from app.api.search import (
    router as search_router
)

from app.api.auth import router as auth_router

app = FastAPI(
    title="Enterprise Knowledge Intelligence Platform",
    version="1.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]
allowed_origins.extend([
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "http://0.0.0.0:4173",
    "http://[::1]:4173",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173",
    "http://[::1]:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.(vercel|netlify|github)\.(app|dev)|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(
    document_summary_router
)
app.include_router(
    search_router
)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(
    chat_history_router
)
app.include_router(history_router)
app.include_router(insights_router)
app.include_router(
    graph_router
)
app.include_router(
    documents_router
)

@app.get("/")
def root():
    return {
        "message": "EKPI backend running!"
        }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.routes import chat, health
from app.knowledge.vector_store import initialize_vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    # Startup
    print("🚀 Initializing Camaral ChatBot...")
    await initialize_vector_store()
    print("✅ Vector store initialized")
    yield
    # Shutdown
    print("👋 Shutting down Camaral ChatBot...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema multiagente para Camaral - Avatares AI para ventas y soporte",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
async def root():
    return {
        "message": "🤖 Camaral ChatBot API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

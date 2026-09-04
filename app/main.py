"""Start the FastAPI application."""

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.news import router as news_router


app = FastAPI(
    title="AI News API",
    description="API for collecting and enriching AI news.",
    version="1.0.0",
)


app.include_router(health_router)
app.include_router(news_router)
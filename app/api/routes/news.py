"""News API endpoints."""

import json

from fastapi import APIRouter, HTTPException

from app.database.repository import get_news_item, get_news_items


router = APIRouter()


@router.get("/news/")
def get_all_news() -> list[dict]:
    """Return all stored news articles without full article content."""

    items = get_news_items()

    return [
        {
            "id": item.id,
            "title": item.title,
            "url": item.url,
            "source": item.source,
            "summary": item.summary,
            "tags": json.loads(item.tags) if item.tags else [],
        }
        for item in items
    ]


@router.get("/news/{news_id}")
def get_single_news(news_id: int) -> dict:
    """Return one news article by ID, including full content."""

    item = get_news_item(news_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="News item not found",
        )

    return {
        "id": item.id,
        "title": item.title,
        "url": item.url,
        "source": item.source,
        "content": item.content,
        "summary": item.summary,
        "tags": json.loads(item.tags) if item.tags else [],
    }
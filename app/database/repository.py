"""Read/write news in the database."""

import json

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.models import NewsItemDB


def save_news_item(
    title: str,
    url: str,
    source: str,
    content: str,
    published_at=None,
    summary: str | None = None,
    tags: list[str] | None = None,
) -> NewsItemDB | None:
    """Save a news item if the URL does not already exist."""

    with SessionLocal() as session:
        existing = session.scalar(
            select(NewsItemDB).where(NewsItemDB.url == url)
        )

        if existing:
            return None

        item = NewsItemDB(
            title=title,
            url=url,
            source=source,
            content=content,
            published_at=published_at,
            summary=summary,
            tags=json.dumps(tags) if tags else None,
        )

        session.add(item)
        session.commit()
        session.refresh(item)

        return item


def get_news_item(news_id: int) -> NewsItemDB | None:
    """Get one news item by ID."""

    with SessionLocal() as session:
        return session.get(NewsItemDB, news_id)


def get_news_items() -> list[NewsItemDB]:
    """Get all news items."""

    with SessionLocal() as session:
        return list(
            session.scalars(
                select(NewsItemDB).order_by(NewsItemDB.id.desc())
            )
        )


def get_unenriched_news() -> list[NewsItemDB]:
    """Get news items that do not have an LLM summary yet."""

    with SessionLocal() as session:
        return list(
            session.scalars(
                select(NewsItemDB).where(NewsItemDB.summary.is_(None))
            )
        )


def update_news_enrichment(
    news_id: int,
    summary: str,
    tags: list[str],
) -> NewsItemDB | None:
    """Update an existing news item with its enrichment."""

    with SessionLocal() as session:
        item = session.get(NewsItemDB, news_id)

        if item is None:
            return None

        item.summary = summary
        item.tags = json.dumps(tags)

        session.commit()
        session.refresh(item)

        return item
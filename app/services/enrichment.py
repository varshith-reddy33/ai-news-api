"""Enrich stored news articles using an LLM."""

import json

from app.agents.news_agent import enrich_news
from app.database.repository import (
    get_unenriched_news,
    update_news_enrichment,
)
from app.schemas.news import NewsItem


def enrich_stored_news() -> None:
    """Find unenriched news and generate summaries and tags."""

    items = get_unenriched_news()

    print(f"Found {len(items)} articles to enrich.")

    for item in items:
        news_item = NewsItem(
            title=item.title,
            url=item.url,
            content=item.content,
        )

        enrichment = enrich_news(news_item)

        update_news_enrichment(
            news_id=item.id,
            summary=enrichment.summary,
            tags=enrichment.tags,
        )

        print(f"Enriched: {item.title}")
        print(f"Summary: {enrichment.summary}")
        print(f"Tags: {json.dumps(enrichment.tags)}")
        print()


if __name__ == "__main__":
    enrich_stored_news()
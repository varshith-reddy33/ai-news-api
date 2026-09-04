"""Ingest news from external sources into PostgreSQL."""

from app.database.repository import save_news_item
from app.scrapers.openai import scrape


def ingest_news() -> None:
    """Scrape news and save new articles to PostgreSQL."""

    items = scrape()

    saved_count = 0
    skipped_count = 0

    for item in items:
        saved_item = save_news_item(
            title=item.title,
            url=str(item.url),
            source="Hacker News",
            content=item.content,
        )

        if saved_item:
            saved_count += 1
            print(f"Saved: {item.title}")
        else:
            skipped_count += 1
            print(f"Skipped duplicate: {item.title}")

    print(
        f"\nIngestion complete: "
        f"{saved_count} saved, {skipped_count} duplicates skipped."
    )


if __name__ == "__main__":
    ingest_news()
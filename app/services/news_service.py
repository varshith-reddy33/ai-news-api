import json
from pathlib import Path

from app.agents.news_agent import enrich_news
from app.schemas.news import NewsEnrichment, NewsItem
from app.scrapers.openai import scrape


OUTPUT_FILE = Path("data/enriched_news.json")


def process_news() -> list[NewsEnrichment]:
    items = scrape()

    results = []

    for item in items:
        enrichment = enrich_news(item)
        results.append(enrichment)

    return results


def save_results(results: list[NewsEnrichment]) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = [
        {
            "summary": result.summary,
            "tags": result.tags,
        }
        for result in results
    ]

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def test_agent_with_sample_news() -> list[NewsEnrichment]:
    items = [
        NewsItem(
            title="OpenAI releases a new AI model",
            url="https://example.com/openai",
            content="OpenAI released a new artificial intelligence model with improved capabilities.",
        ),
        NewsItem(
            title="New database technology improves performance",
            url="https://example.com/database",
            content="A new database technology improves query performance and reduces processing time.",
        ),
    ]

    results = []

    for item in items:
        enrichment = enrich_news(item)
        results.append(enrichment)

    return results


if __name__ == "__main__":
    results = process_news()

    print(f"Processed {len(results)} articles")

    for result in results:
        print(result)

    save_results(results)

    print(f"Saved results to {OUTPUT_FILE}")
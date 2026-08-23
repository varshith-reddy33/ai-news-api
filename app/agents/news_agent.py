from app.schemas.news import NewsEnrichment, NewsItem


def enrich_news(item: NewsItem) -> NewsEnrichment:
    instruction = f"""
    Summarize the news article.
    Focus only on the main context.
    Avoid irrelevant information.
    Return around 4 relevant tags.

    Article title:
    {item.title}

    Article content:
    {item.content}
    """

    tags = ["Technology"]

    if "AI" in item.title or "ai" in item.title:
        tags.append("AI")

    return NewsEnrichment(
        summary=item.title,
        tags=tags,
    )


if __name__ == "__main__":
    item = NewsItem(
        title="Test AI News",
        url="https://example.com",
        content="This is test content.",
    )

    enrichment = enrich_news(item)

    print(enrichment)
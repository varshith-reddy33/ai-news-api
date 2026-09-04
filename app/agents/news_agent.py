"""LLM agent for enriching news articles."""

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.news import NewsEnrichment, NewsItem


load_dotenv()

client = OpenAI()


def enrich_news(item: NewsItem) -> NewsEnrichment:
    """Generate a summary and tags using OpenAI."""

    instruction = f"""
Summarize the following news article.

Requirements:
- Focus only on the main context.
- Keep the summary concise.
- Avoid irrelevant information.
- Return around 4 relevant tags.

Article title:
{item.title}

Article content:
{item.content}
"""

    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "user",
                "content": instruction,
            }
        ],
        text_format=NewsEnrichment,
    )

    return response.output_parsed


if __name__ == "__main__":
    item = NewsItem(
        title="Test AI News",
        url="https://example.com",
        content="This is test content about artificial intelligence.",
    )

    enrichment = enrich_news(item)

    print(enrichment)
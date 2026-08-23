import pytest

from app.agents.news_agent import enrich_news
from app.schemas.news import NewsEnrichment, NewsItem
from app.services import news_service


def test_enrich_news():
    item = NewsItem(
        title="OpenAI releases a new AI model",
        url="https://example.com",
        content="OpenAI released a new artificial intelligence model.",
    )

    result = enrich_news(item)

    assert result.summary == "OpenAI releases a new AI model"
    assert "Technology" in result.tags


def test_news_item_validation():
    item = NewsItem(
        title="Test News",
        url="https://example.com",
        content="Test content",
    )

    assert item.title == "Test News"
    assert item.url == "https://example.com"
    assert item.content == "Test content"


def test_news_item_rejects_invalid_tags():
    with pytest.raises(Exception):
        NewsEnrichment(
            summary="Test summary",
            tags=123,
        )


def test_process_news(monkeypatch):
    sample_items = [
        NewsItem(
            title="Test AI News",
            url="https://example.com",
            content="This is test content.",
        ),
        NewsItem(
            title="Test Database News",
            url="https://example.com/database",
            content="This is database content.",
        ),
    ]

    monkeypatch.setattr(
        news_service,
        "scrape",
        lambda: sample_items,
    )

    results = news_service.process_news()

    assert len(results) == 2
    assert results[0].summary == "Test AI News"
    assert results[1].summary == "Test Database News"


def test_save_results(tmp_path, monkeypatch):
    results = [
        NewsEnrichment(
            summary="Test summary",
            tags=["AI", "Technology"],
        ),
        NewsEnrichment(
            summary="Another summary",
            tags=["Database"],
        ),
    ]

    output_file = tmp_path / "enriched_news.json"

    monkeypatch.setattr(
        news_service,
        "OUTPUT_FILE",
        output_file,
    )

    news_service.save_results(results)

    assert output_file.exists()

    saved_data = output_file.read_text(encoding="utf-8")

    assert "Test summary" in saved_data
    assert "Another summary" in saved_data
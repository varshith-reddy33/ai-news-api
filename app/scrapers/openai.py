import requests

from bs4 import BeautifulSoup

from app.schemas.news import NewsItem


def scrape() -> list[NewsItem]:
    """Scrape top Hacker News stories and return normalized news items."""

    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json",
        timeout=10,
    )
    response.raise_for_status()

    story_ids = response.json()[:5]

    items: list[NewsItem] = []

    for story_id in story_ids:
        try:
            story_response = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=10,
            )
            story_response.raise_for_status()

            story = story_response.json()
            article_url = story.get("url")

            if not article_url:
                continue

            article_response = requests.get(
                article_url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 AI-News-API/1.0"
                },
            )
            article_response.raise_for_status()

        except requests.RequestException:
            continue

        soup = BeautifulSoup(article_response.text, "html.parser")

        # Remove elements that don't contain useful article text.
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()

        # Try common article containers.
        article = (
            soup.find("article")
            or soup.find("main")
            or soup.find("div", class_="entry-content")
            or soup.body
        )

        if not article:
            continue

        paragraphs = article.find_all("p")

        content = "\n".join(
            paragraph.get_text(" ", strip=True)
            for paragraph in paragraphs
        )

        # Some pages don't use <p> tags, so use the container text as fallback.
        if not content:
            content = article.get_text(" ", strip=True)

        if not content:
            continue

        news_item = NewsItem(
            title=story["title"],
            url=article_url,
            content=content,
        )

        items.append(news_item)

    return items


if __name__ == "__main__":
    items = scrape()

    print(f"Scraped {len(items)} articles")

    for item in items:
        print(item.title)
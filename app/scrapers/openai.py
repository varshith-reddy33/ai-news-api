import requests

from bs4 import BeautifulSoup

from app.schemas.news import NewsItem


def scrape() -> list[NewsItem]:
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json",
        timeout=10,
    )

    response.raise_for_status()

    story_ids = response.json()[:5]

    items = []

    for story_id in story_ids:
        story_response = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
            timeout=10,
        )

        story_response.raise_for_status()

        story = story_response.json()

        article_url = story.get("url")

        if not article_url:
            continue

        try:
            article_response = requests.get(
                article_url,
                timeout=10,
            )

            article_response.raise_for_status()

        except requests.RequestException:
            continue

        article_html = article_response.text

        soup = BeautifulSoup(article_html, "html.parser")

        article = soup.find("div", class_="entry-content")

        if not article:
            continue

        paragraphs = article.find_all("p")

        content = "\n".join(
            paragraph.get_text(" ", strip=True)
            for paragraph in paragraphs
        )

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
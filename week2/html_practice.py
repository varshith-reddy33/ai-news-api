import requests
from bs4 import BeautifulSoup

from app.schemas.news import NewsItem


url = "http://www.os2museum.com/wp/the-end-of-an-athlon/"

html = requests.get(url, timeout=10).text

soup = BeautifulSoup(html, "html.parser")

article = soup.find("div", class_="entry-content")

paragraphs = article.find_all("p")

content = "\n".join(
    paragraph.get_text(" ", strip=True)
    for paragraph in paragraphs
)

news_item = NewsItem(
    title=soup.title.get_text(" ", strip=True),
    url=url,
    content=content,
)

print(news_item)
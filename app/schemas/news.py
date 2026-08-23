from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    url: str
    content: str


class NewsEnrichment(BaseModel):
    summary: str
    tags: list[str]
from pydantic import BaseModel


class NewsEnrichment(BaseModel):
    summary: str
    tags: list[str]


result = NewsEnrichment(
    summary="OpenAI released a new AI model.",
    tags=["AI", "OpenAI", "Technology"],
)

print(result)
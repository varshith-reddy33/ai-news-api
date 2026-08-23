from pydantic import BaseModel


class Topic(BaseModel):
    name: str
    relevance: str


class NewsEnrichment(BaseModel):
    summary: str
    topics: list[Topic]


result = NewsEnrichment(
    summary="OpenAI released a new AI model.",
    topics=[
        Topic(
            name="Artificial Intelligence",
            relevance="Main topic"
        ),
        Topic(
            name="OpenAI",
            relevance="Company involved"
        ),
    ],
)

print(result)
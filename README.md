# AI News API

An AI-powered news pipeline that collects articles from Hacker News,
uses OpenAI to generate summaries and tags, stores the enriched data
in PostgreSQL, and exposes it through a FastAPI backend.

## Project Flow

Hacker News
    ↓
Scraper
    ↓
Pydantic Schema
    ↓
OpenAI LLM
    ↓
PostgreSQL
    ↓
FastAPI

## Technologies

- Python
- Pydantic
- OpenAI API
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- uv
- Git & GitHub

## Current Features

- Scrapes news from Hacker News
- Normalizes articles using Pydantic
- Generates summaries and tags using OpenAI
- Stores articles in PostgreSQL
- Prevents duplicate articles using URL
- Provides FastAPI endpoints
- Swagger/OpenAPI documentation
- Handles article content extraction, including arXiv articles

## API Endpoints

GET `/health/`

GET `/news/`

GET `/news/{news_id}`

## Running Locally

Start PostgreSQL:

`docker compose -f week3/database-setup/docker/docker-compose.yml up -d`

Create database tables:

`uv run python -m app.database.create_tables`

Run ingestion:

`uv run python -m app.services.ingestion`

Run enrichment:

`uv run python -m app.services.enrichment`

Start the API:

`uv run uvicorn app.main:app --port 8001`

Swagger:

`http://localhost:8001/docs`

## Status

🚧 Ongoing project — currently developed as part of an AI Engineering learning program.

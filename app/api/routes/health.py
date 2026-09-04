"""Check that the API is running."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/health/")
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}

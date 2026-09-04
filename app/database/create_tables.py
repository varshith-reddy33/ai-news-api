"""Create database tables."""

from app.database.connection import Base, engine
from app.database.models import NewsItemDB


def create_tables() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
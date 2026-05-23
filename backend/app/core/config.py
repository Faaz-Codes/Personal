import os

# Works with docker-compose (host=db) when DATABASE_URL is provided.
# Local fallback points to localhost PostgreSQL for easy first-time setup.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/cattrends",
)

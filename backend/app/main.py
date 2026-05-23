from fastapi import FastAPI

from app.api.routes.audios import router as audios_router
from app.api.routes.videos import router as videos_router
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.services.mock_data import generate_mock_videos

app = FastAPI(title="Viral Cat Trend Radar API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    # Seed local mock rows so the API has useful data immediately.
    db = SessionLocal()
    try:
        generate_mock_videos(db, count=30)
    finally:
        db.close()


app.include_router(videos_router)
app.include_router(audios_router)


@app.get("/health")
def health():
    return {"status": "healthy"}

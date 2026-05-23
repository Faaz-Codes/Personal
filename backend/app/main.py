from fastapi import FastAPI

from app.api.routes.videos import router as videos_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Viral Cat Trend Radar API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(videos_router)


@app.get("/health")
def health():
    return {"status": "healthy"}

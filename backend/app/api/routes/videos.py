from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Video
from app.schemas.video import VideoOut
from app.services.ingest import refresh_scrape
from app.services.mock_data import generate_mock_videos

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("/trending", response_model=list[VideoOut])
def trending(db: Session = Depends(get_db)):
    return db.scalars(select(Video).order_by(desc(Video.trend_score)).limit(50)).all()


@router.get("/exploding", response_model=list[VideoOut])
def exploding(db: Session = Depends(get_db)):
    return db.scalars(
        select(Video)
        .where(Video.views > 10000)
        .order_by(desc(Video.comments), desc(Video.shares))
        .limit(20)
    ).all()


@router.post("/refresh")
async def refresh(db: Session = Depends(get_db)):
    count = await refresh_scrape(db)
    return {"status": "ok", "processed": count}


@router.post("/mock/generate")
def generate_mock(db: Session = Depends(get_db), count: int = 60):
    inserted = generate_mock_videos(db=db, count=count)
    return {"status": "ok", "inserted": inserted}

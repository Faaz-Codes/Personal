from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Video
from app.schemas.video import VideoOut
from app.services.ingest import refresh_scrape

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("/trending", response_model=list[VideoOut])
def trending(db: Session = Depends(get_db)):
    return db.scalars(select(Video).order_by(desc(Video.trend_score)).limit(50)).all()


@router.get("/exploding", response_model=list[VideoOut])
def exploding(db: Session = Depends(get_db)):
    return db.scalars(select(Video).where(Video.views > 10000).order_by(desc(Video.comments)).limit(20)).all()


@router.get("/top-audios")
def top_audios(db: Session = Depends(get_db)):
    videos = db.scalars(select(Video).order_by(desc(Video.trend_score)).limit(100)).all()
    audio_map: dict[str, int] = {}
    for video in videos:
        if not video.audio_name:
            continue
        audio_map[video.audio_name] = audio_map.get(video.audio_name, 0) + 1
    return [{"audio_name": k, "count": v} for k, v in sorted(audio_map.items(), key=lambda x: x[1], reverse=True)[:20]]


@router.post("/refresh")
async def refresh(db: Session = Depends(get_db)):
    count = await refresh_scrape(db)
    return {"status": "ok", "processed": count}

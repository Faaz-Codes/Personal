from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Video

router = APIRouter(prefix="/audios", tags=["audios"])


@router.get("/top")
def top_audios(db: Session = Depends(get_db)):
    videos = db.scalars(select(Video).order_by(desc(Video.trend_score)).limit(100)).all()

    audio_usage: dict[str, int] = {}
    for video in videos:
        if not video.audio_name:
            continue
        audio_usage[video.audio_name] = audio_usage.get(video.audio_name, 0) + 1

    ranked = sorted(audio_usage.items(), key=lambda item: item[1], reverse=True)
    return [{"audio_name": name, "count": count} for name, count in ranked[:20]]

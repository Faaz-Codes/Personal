from __future__ import annotations

from datetime import datetime, timedelta
from random import choice, randint

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Video
from app.services.trend import calculate_trend_score

PLATFORMS = ["tiktok", "instagram", "youtube_shorts", "reddit"]
AUDIO_NAMES = [
    "Meow Beats",
    "Cat Zoomies Remix",
    "Purr Lo-fi",
    "Tiny Tiger Trap",
    "Keyboard Cat 2.0",
]
CAPTIONS = [
    "Orange cat discovers cardboard castle",
    "Kitten learns to high-five",
    "Rescue cat's first day home",
    "Cat politely asks for treats",
    "Maine coon dramatic flop",
]


def generate_mock_videos(db: Session, count: int = 60) -> int:
    """Populate the videos table with beginner-friendly mock data.

    - Skips URLs that already exist.
    - Recomputes trend_score from generated metrics.
    - Returns the number of newly inserted rows.
    """
    inserted = 0
    now = datetime.utcnow()

    for i in range(count):
        platform = choice(PLATFORMS)
        views = randint(1_000, 2_000_000)
        likes = randint(100, max(views // 4, 100))
        comments = randint(10, max(views // 40, 10))
        shares = randint(5, max(views // 60, 5))
        followers = randint(500, 3_000_000)

        url = f"https://example.com/{platform}/video-{i}"
        exists = db.scalar(select(Video.id).where(Video.url == url))
        if exists:
            continue

        posted_at = now - timedelta(hours=randint(1, 120))
        video = Video(
            platform=platform,
            url=url,
            caption=choice(CAPTIONS),
            hashtags=["#cat", "#viral", "#pet"],
            views=views,
            likes=likes,
            comments=comments,
            shares=shares,
            audio_name=choice(AUDIO_NAMES),
            creator_name=f"creator_{platform}_{i}",
            followers=followers,
            posted_at=posted_at,
            thumbnail_url="https://picsum.photos/seed/cat/480/640",
            trend_score=calculate_trend_score(views, likes, comments, shares, followers),
        )
        db.add(video)
        inserted += 1

    if inserted:
        db.commit()

    return inserted

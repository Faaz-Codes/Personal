import asyncio
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Video
from app.scrapers.platforms import InstagramScraper, RedditScraper, TikTokScraper, YouTubeShortsScraper
from app.services.trend import calculate_trend_score


async def refresh_scrape(db: Session) -> int:
    scrapers = [RedditScraper(), YouTubeShortsScraper(), TikTokScraper(), InstagramScraper()]
    batches = await asyncio.gather(*[s.scrape() for s in scrapers])
    count = 0
    for videos in batches:
        for v in videos:
            existing = db.scalar(select(Video).where(Video.url == v["url"]))
            score = calculate_trend_score(v["views"], v["likes"], v["comments"], v["shares"], v["followers"])
            if existing:
                for key, value in v.items():
                    setattr(existing, key, value)
                existing.trend_score = score
                existing.scraped_at = datetime.utcnow()
            else:
                db.add(Video(**v, trend_score=score))
            count += 1
    db.commit()
    return count

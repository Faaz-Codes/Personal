from datetime import datetime

from pydantic import BaseModel


class VideoOut(BaseModel):
    id: int
    platform: str
    url: str
    caption: str | None = None
    hashtags: list[str] | None = None
    views: int
    likes: int
    comments: int
    shares: int
    audio_name: str | None = None
    creator_name: str | None = None
    followers: int
    posted_at: datetime | None = None
    scraped_at: datetime
    trend_score: float
    thumbnail_url: str | None = None
    media_url: str | None = None
    post_age: str | None = None
    subreddit: str | None = None

    class Config:
        from_attributes = True

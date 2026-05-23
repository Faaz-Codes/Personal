from datetime import datetime, timedelta

from app.scrapers.base import BaseScraper


class RedditScraper(BaseScraper):
    platform = "reddit"

    async def scrape(self) -> list[dict]:
        return [{"platform": self.platform, "url": "https://reddit.com/r/cats/sample1", "caption": "Cat zoomies", "hashtags": ["cats", "catsoftiktok"], "views": 12000, "likes": 1400, "comments": 120, "shares": 90, "audio_name": "N/A", "creator_name": "u/catlover", "followers": 5000, "posted_at": datetime.utcnow() - timedelta(hours=2), "thumbnail_url": None}]


class YouTubeShortsScraper(BaseScraper):
    platform = "youtube"

    async def scrape(self) -> list[dict]:
        return [{"platform": self.platform, "url": "https://youtube.com/shorts/sample2", "caption": "Funny kitten", "hashtags": ["cat", "kitten"], "views": 22000, "likes": 2400, "comments": 250, "shares": 110, "audio_name": "Original", "creator_name": "Cat Channel", "followers": 12000, "posted_at": datetime.utcnow() - timedelta(hours=4), "thumbnail_url": None}]


class TikTokScraper(BaseScraper):
    platform = "tiktok"

    async def scrape(self) -> list[dict]:
        return [{"platform": self.platform, "url": "https://tiktok.com/@cats/video/sample3", "caption": "Cat trend", "hashtags": ["cattrend", "cats"], "views": 45000, "likes": 3900, "comments": 410, "shares": 350, "audio_name": "Viral Cat Audio", "creator_name": "cattok", "followers": 18000, "posted_at": datetime.utcnow() - timedelta(hours=1), "thumbnail_url": None}]


class InstagramScraper(BaseScraper):
    platform = "instagram"

    async def scrape(self) -> list[dict]:
        return [{"platform": self.platform, "url": "https://instagram.com/reel/sample4", "caption": "Placeholder reel scraper", "hashtags": ["cats", "reels"], "views": 8000, "likes": 700, "comments": 60, "shares": 20, "audio_name": "Placeholder Audio", "creator_name": "instacats", "followers": 9000, "posted_at": datetime.utcnow() - timedelta(hours=6), "thumbnail_url": None}]

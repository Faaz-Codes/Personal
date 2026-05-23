from datetime import datetime, timedelta
from typing import Any

import httpx

from app.scrapers.base import BaseScraper


class RedditScraper(BaseScraper):
    platform = "reddit"

    SUBREDDITS = ["cats", "OneOrangeBraincell", "CatsAreAssholes", "StartledCats"]

    @staticmethod
    def _age_from_created(created_utc: float) -> str:
        delta = datetime.utcnow() - datetime.utcfromtimestamp(created_utc)
        if delta < timedelta(minutes=1):
            return "just now"
        if delta < timedelta(hours=1):
            return f"{int(delta.total_seconds() // 60)}m"
        if delta < timedelta(days=1):
            return f"{int(delta.total_seconds() // 3600)}h"
        return f"{delta.days}d"

    @staticmethod
    def _extract_media_url(post: dict[str, Any]) -> str | None:
        if post.get("url_overridden_by_dest"):
            return post["url_overridden_by_dest"]
        if post.get("url"):
            return post["url"]
        preview = post.get("preview") or {}
        images = preview.get("images") or []
        if images:
            source = images[0].get("source") or {}
            if source.get("url"):
                return source["url"].replace("&amp;", "&")
        return None

    async def scrape(self) -> list[dict]:
        seen: set[tuple[str, str]] = set()
        scraped_posts: list[dict[str, Any]] = []
        headers = {"User-Agent": "CatTrendRadarBot/1.0"}

        async with httpx.AsyncClient(timeout=20, headers=headers) as client:
            for subreddit in self.SUBREDDITS:
                response = await client.get(
                    f"https://www.reddit.com/r/{subreddit}/hot.json",
                    params={"limit": 50},
                )
                response.raise_for_status()
                children = response.json().get("data", {}).get("children", [])
                for child in children:
                    post = child.get("data", {})
                    post_id = post.get("id")
                    title = post.get("title")
                    author = post.get("author")
                    if not post_id or not title:
                        continue

                    dedupe_key = (post_id, author or "")
                    if dedupe_key in seen:
                        continue
                    seen.add(dedupe_key)

                    created_utc = float(post.get("created_utc", datetime.utcnow().timestamp()))
                    permalink = post.get("permalink") or ""
                    media_url = self._extract_media_url(post)

                    scraped_posts.append(
                        {
                            "platform": self.platform,
                            "url": f"https://reddit.com{permalink}",
                            "caption": title,
                            "hashtags": [f"r/{subreddit}"],
                            "views": int(post.get("view_count") or 0),
                            "likes": int(post.get("ups") or 0),
                            "comments": int(post.get("num_comments") or 0),
                            "shares": 0,
                            "audio_name": None,
                            "creator_name": author,
                            "followers": 0,
                            "posted_at": datetime.utcfromtimestamp(created_utc),
                            "thumbnail_url": post.get("thumbnail") if str(post.get("thumbnail", "")).startswith("http") else None,
                            "media_url": media_url,
                            "post_age": self._age_from_created(created_utc),
                            "subreddit": subreddit,
                        }
                    )

        return scraped_posts


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

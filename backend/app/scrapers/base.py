from abc import ABC, abstractmethod


class BaseScraper(ABC):
    platform: str

    @abstractmethod
    async def scrape(self) -> list[dict]:
        raise NotImplementedError

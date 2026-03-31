from abc import ABC, abstractmethod
from typing import List

class BaseScraper(ABC):
    @abstractmethod
    async def get_jobs(self, keywords: str, location: str) -> List[dict]:
        """Fetch jobs matching keywords and location."""
        pass

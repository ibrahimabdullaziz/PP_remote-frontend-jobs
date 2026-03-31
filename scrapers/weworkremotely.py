import httpx
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import urllib.parse

class WWRScraper(BaseScraper):
    def __init__(self):
        self.base_url = "https://weworkremotely.com/remote-jobs/search"
        
    async def get_jobs(self, keywords: str, location: str):
        # Strategy placeholder
        return []

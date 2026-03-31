import httpx
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
from loguru import logger
from utils.date_utils import get_age_hours
import feedparser

class WWRScraper(BaseScraper):
    def __init__(self):
        # We Work Remotely provides an excellent RSS feed for frontend jobs which is faster and more reliable than HTML scraping
        self.rss_url = "https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss"
        
    async def get_jobs(self, keywords: str, location: str):
        # Note: WWR is global by default and categorized. We don't strictly use the LinkedIn profile 'location' or 'keywords' 
        # because the RSS stream is already perfectly filtered for Remote Frontend.
        jobs = []
        try:
            logger.info(f"Fetching WWR RSS Feed: {self.rss_url}")
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(self.rss_url)
                
            if res.status_code == 200:
                feed = feedparser.parse(res.text)
                for entry in feed.entries:
                    # Extract Data
                    title_raw = entry.title
                    # The WWR RSS title is formatted as "Company Name: Job Title"
                    if ":" in title_raw:
                        company = title_raw.split(":")[0].strip()
                        title = title_raw.split(":", 1)[1].strip()
                    else:
                        company = "WWR Employer"
                        title = title_raw

                    link = entry.link
                    # ID is usually in the URL
                    job_id = link.split("-")[-1] if "-" in link else link.split("/")[-1]
                    
                    jobs.append({
                        "id": f"wwr_{job_id}",
                        "title": title,
                        "company": company,
                        "location": "Global / Remote",
                        "url": link,
                        "description": entry.get('description', entry.get('summary', '')),
                        "time_posted": entry.get('published', 'Recently'),
                        "age_hours": get_age_hours(entry.get('published', 'Recently')),
                        "platform": "We Work Remotely"
                    })
                logger.info(f"WWR Extraction Complete. Found {len(jobs)} global roles.")
            else:
                logger.warning(f"WWR returned non-200 status: {res.status_code}")
        except Exception as e:
            logger.error(f"WWR Scraper Exception: {e}")
            raise e
        return jobs

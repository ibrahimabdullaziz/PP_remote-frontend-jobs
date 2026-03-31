import httpx
from scrapers.base import BaseScraper
from loguru import logger
from utils.date_utils import get_age_hours

class HimalayasScraper(BaseScraper):
    def __init__(self):
        # Himalayas open API endpoint
        self.api_url = "https://himalayas.app/jobs/api?limit=100"
        
    async def get_jobs(self, keywords: str, location: str):
        jobs = []
        try:
            logger.info(f"Fetching Himalayas API: {self.api_url}")
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(self.api_url)
                
            if res.status_code == 200:
                data = res.json()
                api_jobs = data.get("jobs", [])
                
                for job in api_jobs:
                    # We stream all 100 recent jobs, and rely on `main.py`'s `is_valid_frontend_job` to drop the NON-frontend ones.
                    jobs.append({
                        "id": f"himalayas_{job.get('guid', job.get('id', 'temp'))}",
                        "title": job.get("title", "Software Engineer"),
                        "company": job.get("companyName", "Tech Company"),
                        "location": "Global / Remote",  # All Himalayas jobs are strictly remote
                        "url": job.get("applicationLink", job.get("jobLink", "")),
                        "description": job.get("description", ""),
                        "time_posted": str(job.get("pubDate", "Recently")),
                        "age_hours": get_age_hours(str(job.get("pubDate", "Recently"))),
                        "platform": "Himalayas"
                    })
                logger.info(f"Himalayas API Extraction Complete. Found {len(jobs)} recent remote roles (pending strict frontend filtering).")
            else:
                logger.warning(f"Himalayas API returned non-200 status: {res.status_code}")
        except Exception as e:
            logger.error(f"Himalayas Scraper Exception: {e}")
        return jobs

import httpx
from scrapers.base import BaseScraper
from loguru import logger
from utils.date_utils import get_age_hours

class RemoteOKScraper(BaseScraper):
    def __init__(self):
        # RemoteOK provides a robust free JSON API perfectly suited for automated extraction
        self.api_url = "https://remoteok.com/api?tag=frontend"
        
    async def get_jobs(self, keywords: str, location: str):
        jobs = []
        try:
            logger.info(f"Fetching RemoteOK API: {self.api_url}")
            # RemoteOK strictly requires a User-Agent, otherwise it returns 403 Forbidden
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(self.api_url, headers=headers)
                
            if res.status_code == 200:
                data = res.json()
                # The first item in RemoteOK is usually API metadata, jobs start from index 1
                api_jobs = data[1:] if len(data) > 1 else []
                
                for job in api_jobs:
                    # RemoteOK occasionally injects ads, filter them by ensuring an 'id' exists
                    if "id" not in job:
                        continue
                        
                    jobs.append({
                        "id": f"remoteok_{job['id']}",
                        "title": job.get("position", "Frontend Developer"),
                        "company": job.get("company", "Global Firm"),
                        "location": job.get("location", "Global / Remote"),
                        "url": job.get("url", ""),
                        "description": job.get("description", ""),
                        "time_posted": job.get("date", "Recently"),
                        "age_hours": get_age_hours(job.get("date", "Recently")),
                        "platform": "RemoteOK"
                    })
                logger.info(f"RemoteOK API Extraction Complete. Found {len(jobs)} global frontend roles.")
            else:
                logger.warning(f"RemoteOK API returned non-200 status: {res.status_code}")
        except Exception as e:
            logger.error(f"RemoteOK Scraper Exception: {e}")
            # We don't raise here because RemoteOK can sometimes blip, we just return empty list to not crash loop
        return jobs

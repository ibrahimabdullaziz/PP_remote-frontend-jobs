import httpx
from scrapers.base import BaseScraper
from loguru import logger

class RemotiveScraper(BaseScraper):
    def __init__(self):
        # Remotive has an open, free API specifically for remote tech jobs
        self.api_url = "https://remotive.com/api/remote-jobs?category=front-end-development"
        
    async def get_jobs(self, keywords: str, location: str):
        jobs = []
        try:
            logger.info(f"Fetching Remotive API: {self.api_url}")
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(self.api_url)
                
            if res.status_code == 200:
                data = res.json()
                api_jobs = data.get("jobs", [])
                
                for job in api_jobs:
                    jobs.append({
                        "id": f"remotive_{job['id']}",
                        "title": job.get("title", "Frontend Developer"),
                        "company": job.get("company_name", "Global Firm"),
                        "location": job.get("candidate_required_location", "Global / Remote"),
                        "url": job.get("url", ""),
                        "description": job.get("description", ""),
                        "time_posted": job.get("publication_date", "Recently").split("T")[0], # formats date to YYYY-MM-DD
                        "platform": "Remotive API"
                    })
                logger.info(f"Remotive API Extraction Complete. Found {len(jobs)} global frontend roles.")
            else:
                logger.warning(f"Remotive API returned non-200 status: {res.status_code}")
        except Exception as e:
            logger.error(f"Remotive Scraper Exception: {e}")
            raise e
        return jobs

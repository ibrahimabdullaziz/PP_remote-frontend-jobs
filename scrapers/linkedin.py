import asyncio
import random
import urllib.parse
from playwright.async_api import async_playwright
from scrapers.base import BaseScraper

class LinkedInScraper(BaseScraper):
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs/search"
        
    async def get_jobs(self, keywords: str, location: str):
        jobs = []
        params = {
            "keywords": keywords,
            "location": location,
            "f_WRA": "true",       # Remote
            "f_TPR": "r86400",     # Past 24 hours
            "position": 1,
            "pageNum": 0
        }
        
        query_string = urllib.parse.urlencode(params)
        target_url = f"{self.base_url}?{query_string}"

        async with async_playwright() as p:
            # Using Chromium with evasions (Anti-bot measures)
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            try:
                await page.goto(target_url, wait_until="domcontentloaded")
                
                # Jitter delay to mimic human behavior
                await asyncio.sleep(random.uniform(2.0, 5.0))
                
                # Parse job cards (Guest View Layout)
                items = await page.query_selector_all('ul.jobs-search__results-list > li')
                for item in items:
                    job_id = await item.get_attribute("data-entity-urn")
                    if not job_id:
                        continue
                        
                    title_elem = await item.query_selector('h3.base-search-card__title')
                    company_elem = await item.query_selector('h4.base-search-card__subtitle')
                    url_elem = await item.query_selector('a.base-card__full-link')
                    time_elem = await item.query_selector('time')
                    
                    if title_elem and company_elem and url_elem:
                        time_text = (await time_elem.inner_text()).strip() if time_elem else 'Recently'
                        jobs.append({
                            "id": f"linkedin_{job_id.split(':')[-1]}",
                            "title": (await title_elem.inner_text()).strip(),
                            "company": (await company_elem.inner_text()).strip(),
                            "location": location,
                            "url": await url_elem.get_attribute('href'),
                            "time_posted": time_text,
                            "platform": "LinkedIn"
                        })
            except Exception as e:
                print(f"LinkedIn Scraper Exception: {e}")
            finally:
                await browser.close()
                
        return jobs

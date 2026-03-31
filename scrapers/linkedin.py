import asyncio
import random
import urllib.parse
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import httpx
from bs4 import BeautifulSoup
from loguru import logger
from scrapers.base import BaseScraper
from config.settings import PROXIES, FAKE_REMOTE_KEYWORDS

class LinkedInScraper(BaseScraper):
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs/search"
        
    async def fetch_job_description(self, url: str) -> str:
        """Fetch the job full description quickly via HTTPX for filtering."""
        try:
            # We don't always need proxy here, but could use one. We'll use random header.
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=10.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    desc_div = soup.find('div', class_='show-more-less-html__markup')
                    if desc_div:
                        return desc_div.get_text(separator=' ', strip=True).lower()
        except Exception as e:
            logger.warning(f"Failed to fetch job description for {url}: {e}")
        return ""

    def is_fake_remote(self, text: str) -> bool:
        """Check if job description triggers any fake remote keywords."""
        if not text:
            return False
        for kw in FAKE_REMOTE_KEYWORDS:
            if kw.lower() in text:
                return True
        return False

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
            # Proxy Selection
            proxy_opt = None
            if PROXIES:
                p_url = random.choice(PROXIES)
                proxy_opt = {"server": p_url}
                logger.debug(f"Using proxy: {p_url.split('@')[-1] if '@' in p_url else p_url}")

            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                proxy=proxy_opt
            )
            page = await context.new_page()
            
            # Apply Playwright Stealth
            await stealth_async(page)
            
            try:
                logger.info(f"Navigating to {target_url}")
                await page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
                
                # Jitter delay to mimic human behavior
                await asyncio.sleep(random.uniform(2.0, 5.0))
                
                # Parse job cards (Guest View Layout)
                items = await page.query_selector_all('ul.jobs-search__results-list > li')
                logger.info(f"Found {len(items)} job cards on page.")
                
                for item in items:
                    job_id = await item.get_attribute("data-entity-urn")
                    if not job_id:
                        continue
                        
                     title_elem = await item.query_selector('h3.base-search-card__title, .base-card__title, .result-card__title')
                    company_elem = await item.query_selector('h4.base-search-card__subtitle, .base-card__subtitle, .result-card__subtitle-link')
                    url_elem = await item.query_selector('a.base-card__full-link, .result-card__full-link')
                    time_elem = await item.query_selector('time, .job-result-card__list-date')
                    
                    if not title_elem or not company_elem or not url_elem:
                        logger.debug(f"Skipping job card {job_id} - missing elements (T:{bool(title_elem)} C:{bool(company_elem)} U:{bool(url_elem)})")
                        continue

                    title_text = (await title_elem.inner_text()).strip()
                    comp_text = (await company_elem.inner_text()).strip()
                    url_text = await url_elem.get_attribute('href')
                    time_text = (await time_elem.inner_text()).strip() if time_elem else 'Recently'
                    
                    # Apply Title-Level filtering (fast fail)
                    if self.is_fake_remote(title_text.lower() + " " + comp_text.lower()):
                        logger.info(f"Skipping {title_text} at {comp_text} (Title/Company indicates fake remote)")
                        continue
                        
                    # Apply Description-Level filtering (HTTP fetch)
                    desc_text = await self.fetch_job_description(url_text)
                    if self.is_fake_remote(desc_text):
                        logger.info(f"Skipping {title_text} at {comp_text} (Description indicates fake remote)")
                        continue
                    
                    jobs.append({
                        "id": f"linkedin_{job_id.split(':')[-1]}",
                        "title": title_text,
                        "company": comp_text,
                        "location": location,
                        "url": url_text,
                        "time_posted": time_text,
                        "platform": "LinkedIn"
                    })
            except Exception as e:
                logger.error(f"LinkedIn Scraper Exception: {e}")
                raise e # Reraise to be caught by main loop for admin alert
            finally:
                await browser.close()
                
        return jobs

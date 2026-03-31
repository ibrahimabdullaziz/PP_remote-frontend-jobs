import asyncio
import sys
from loguru import logger
from config.settings import POLL_INTERVAL_SECONDS, TARGET_PROFILES, MANDATORY_TITLE_KEYWORDS, FAKE_REMOTE_KEYWORDS
from core.database import init_db, is_job_processed, mark_job_processed
from core.telegram_notifier import send_job_alert, send_admin_alert
from scrapers.linkedin import LinkedInScraper
from scrapers.weworkremotely import WWRScraper
from scrapers.remotive import RemotiveScraper
from scrapers.remoteok import RemoteOKScraper
from scrapers.himalayas import HimalayasScraper

# Setup Loguru for structured, async-friendly logging
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", level="INFO")

def is_valid_frontend_job(title: str) -> bool:
    """Ensure the job strictly matches frontend keywords and contains no fake-remote keywords."""
    title_lower = title.lower()
    
    # Must contain frontend tech
    if not any(kw.lower() in title_lower for kw in MANDATORY_TITLE_KEYWORDS):
        return False
        
    # Must NOT contain backend/fake-remote keywords in title
    for kw in FAKE_REMOTE_KEYWORDS:
        if kw.lower() in title_lower:
            return False
            
    return True

async def process_jobs(jobs):
    """Filter, deduplicate, and notify for a batch of jobs."""
    for job in jobs:
        if not is_valid_frontend_job(job['title']):
            logger.debug(f"Skipping IRRELEVANT title: {job['title']} from {job['platform']}")
            continue
            
        if not await is_job_processed(job["id"]):
            logger.success(f"New Job Found [{job['platform']}]: {job['title']} at {job['company']}")
            await send_job_alert(job)
            await mark_job_processed(job["id"], job["platform"])
            
            # Respectful rate limiting between Telegram alerts
            await asyncio.sleep(1)

async def run_scraper_iteration():
    logger.info("Starting scraping iteration across all platforms...")
    
    # 1. Localized Scrapers (Require Specific Profiles)
    linkedin_scraper = LinkedInScraper()
    for profile in TARGET_PROFILES:
        logger.info(f"LinkedIn: Scraping for keywords: {profile['keywords']} in {profile['location']}")
        jobs = await linkedin_scraper.get_jobs(profile["keywords"], profile["location"])
        await process_jobs(jobs)
        await asyncio.sleep(2)
        
    # 2. Global API Scrapers (No profiles needed, mass extraction)
    global_scrapers = [WWRScraper(), RemotiveScraper(), RemoteOKScraper(), HimalayasScraper()]
    for scraper in global_scrapers:
        try:
            jobs = await scraper.get_jobs("", "")
            await process_jobs(jobs)
        except Exception as e:
            logger.error(f"{scraper.__class__.__name__} failed: {e}")
        await asyncio.sleep(2)

async def main():
    await init_db()
    logger.info("Initialization complete. Entering scheduler loop.")
    await send_admin_alert("✅ Bot Multi-Platform Expansion started successfully. Listening for global remote frontend jobs...")
    
    while True:
        try:
            await run_scraper_iteration()
        except Exception as e:
            logger.critical(f"Fatal error in loop: {e}")
            await send_admin_alert(f"Critical Scraper Failure:\n<code>{e}</code>\nRetrying in {POLL_INTERVAL_SECONDS}s.")
        
        # Wait for the next interval
        logger.info(f"Sleeping for {POLL_INTERVAL_SECONDS} seconds...")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot manually stopped.")

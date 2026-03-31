import asyncio
import sys
from loguru import logger
from config.settings import POLL_INTERVAL_SECONDS, TARGET_PROFILES
from core.database import init_db, is_job_processed, mark_job_processed
from core.telegram_notifier import send_job_alert, send_admin_alert
from scrapers.linkedin import LinkedInScraper

# Setup Loguru for structured, async-friendly logging
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", level="INFO")

async def run_scraper_iteration():
    logger.info("Starting scraping iteration...")
    linkedin_scraper = LinkedInScraper()
    
    for profile in TARGET_PROFILES:
        logger.info(f"Scraping for keywords: {profile['keywords']} in {profile['location']}")
        
        # 1. Scrape
        jobs = await linkedin_scraper.get_jobs(profile["keywords"], profile["location"])
        
        # 2. Process & Deduplicate
        for job in jobs:
            if not await is_job_processed(job["id"]):
                logger.success(f"New Job Found: {job['title']} at {job['company']}")
                await send_job_alert(job)
                await mark_job_processed(job["id"], job["platform"])
                
                # Respectful rate limiting between Telegram alerts
                await asyncio.sleep(1)
        
        # Inter-profile delay
        await asyncio.sleep(2)

async def main():
    await init_db()
    logger.info("Initialization complete. Entering scheduler loop.")
    await send_admin_alert("✅ Bot started successfully. Listening for remote frontend jobs...")
    
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

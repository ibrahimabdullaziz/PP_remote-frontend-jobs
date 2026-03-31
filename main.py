import asyncio
from config.settings import POLL_INTERVAL_SECONDS, TARGET_PROFILES
from core.database import init_db, is_job_processed, mark_job_processed
from core.telegram_notifier import send_job_alert
from scrapers.linkedin import LinkedInScraper

async def run_scraper_iteration():
    print("Starting scraping iteration...")
    linkedin_scraper = LinkedInScraper()
    
    for profile in TARGET_PROFILES:
        print(f"Scraping for keywords: {profile['keywords']} in {profile['location']}")
        # 1. Scrape
        jobs = await linkedin_scraper.get_jobs(profile["keywords"], profile["location"])
        
        # 2. Process & Deduplicate
        for job in jobs:
            if not await is_job_processed(job["id"]):
                print(f"New Job Found: {job['title']} at {job['company']}")
                await send_job_alert(job)
                await mark_job_processed(job["id"], job["platform"])
                
                # Respectful rate limiting between Telegram alerts
                await asyncio.sleep(1)
        
        # Inter-profile delay
        await asyncio.sleep(2)

async def main():
    await init_db()
    print("Initialization complete. Entering scheduler loop.")
    
    while True:
        try:
            await run_scraper_iteration()
        except Exception as e:
            print(f"Fatal error in loop: {e}")
        
        # Wait for the next 5-minute interval
        print(f"Sleeping for {POLL_INTERVAL_SECONDS} seconds...")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from scrapers.linkedin import LinkedInScraper
from scrapers.weworkremotely import WWRScraper
from scrapers.remotive import RemotiveScraper
from scrapers.remoteok import RemoteOKScraper
from scrapers.himalayas import HimalayasScraper
from config.settings import TARGET_PROFILES, MANDATORY_TITLE_KEYWORDS
import json

def is_valid_frontend_job(title: str, description: str = "") -> bool:
    full_text = (title + " " + description).lower()
    return any(kw.lower() in title.lower() for kw in MANDATORY_TITLE_KEYWORDS)

async def test_scrapers():
    scrapers = {
        "LinkedIn": LinkedInScraper(),
        "WWR": WWRScraper(),
        "Remotive": RemotiveScraper(),
        "RemoteOK": RemoteOKScraper(),
        "Himalayas": HimalayasScraper()
    }
    
    results = {}
    
    # Test LinkedIn (first profile)
    profile = TARGET_PROFILES[0]
    print(f"Testing LinkedIn with: {profile['keywords']} in {profile['location']}")
    try:
        jobs = await scrapers["LinkedIn"].get_jobs(profile["keywords"], profile["location"])
        results["LinkedIn"] = {
            "count": len(jobs),
            "sample": jobs[:2] if jobs else []
        }
    except Exception as e:
        results["LinkedIn"] = {"error": str(e)}

    # Test others
    for name, scraper in scrapers.items():
        if name == "LinkedIn": continue
        print(f"Testing {name}...")
        try:
            jobs = await scraper.get_jobs("", "")
            filtered = [j for j in jobs if is_valid_frontend_job(j['title'], j.get('description', ''))]
            results[name] = {
                "total": len(jobs),
                "filtered": len(filtered),
                "sample": filtered[:2] if filtered else []
            }
        except Exception as e:
            results[name] = {"error": str(e)}

    print("\n--- TEST RESULTS ---")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(test_scrapers())

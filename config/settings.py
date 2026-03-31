import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", TELEGRAM_CHAT_ID)
DATABASE_PATH = "data/state.db"

# Proxies for IP Rotation: format "http://username:pass@ip:port"
PROXIES = [p.strip() for p in os.getenv("PROXIES", "").split(",") if p.strip()]

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Scraper Settings
POLL_INTERVAL_SECONDS = 1800 # 30 minutes

# Advanced Filtering: Reject if description matches these keywords
FAKE_REMOTE_KEYWORDS = [
    "hybrid", "on-site", "relocate", "relocation required", 
    "office", "not remote", "us only", "usa only", "clearance"
]

# Default Search Profiles for Remote Frontend Jobs
TARGET_PROFILES = [
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Next.js") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "Worldwide",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Next.js") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "Egypt",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Next.js") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "Saudi Arabia",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Next.js") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "United Arab Emirates",
    }
]

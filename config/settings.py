import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", TELEGRAM_CHAT_ID)
DATABASE_PATH = "data/state.db"
LOG_FILE_PATH = "data/scraper.log"

# Proxies for IP Rotation: format "http://username:pass@ip:port"
PROXIES = [p.strip() for p in os.getenv("PROXIES", "").split(",") if p.strip()]

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Scraper Settings
POLL_INTERVAL_SECONDS = 600 
MAX_JOB_AGE_HOURS = 24

# Advanced Filtering: Reject if description matches these keywords
FAKE_REMOTE_KEYWORDS = [
    "hybrid", "on-site", "relocate", "relocation required", 
    "office-based", "at the office", "not remote", 
    "us only", "usa only", "us permanent", "clearance required",
    "backend", "full-stack", "fullstack", "java", "python", "php", "django", "laravel", "c#", "embedded", "data engineer", "data scientist"
]

# Mandatory Keywords: One of these MUST be in the job title
MANDATORY_TITLE_KEYWORDS = [
    "frontend", "front-end", "react", "next.js", "vue", "javascript", "js", "typescript", "ts",
    "web", "ui", "ux", "developer", "engineer", "software", "senior", "junior", "middle", "staff", "lead"
]

# Default Search Profiles for Remote Frontend Jobs
TARGET_PROFILES = [
    {
        "keywords": "Frontend React Next.js",
        "location": "Egypt",
    },
    {
        "keywords": "Frontend React Next.js",
        "location": "Saudi Arabia",
    },
    {
        "keywords": "Frontend React Next.js",
        "location": "United Arab Emirates",
    }
]

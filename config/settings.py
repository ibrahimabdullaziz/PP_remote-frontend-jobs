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
POLL_INTERVAL_SECONDS = 1250 

# Advanced Filtering: Reject if description matches these keywords
FAKE_REMOTE_KEYWORDS = [
    "hybrid", "on-site", "relocate", "relocation required", 
    "office-based", "at the office", "not remote", 
    "us only", "usa only", "us permanent", "clearance required",
    "backend", "full-stack", "fullstack", "java", "python", "php", "django", "laravel", "c#", "embedded"
]

# Mandatory Keywords: One of these MUST be in the job title
MANDATORY_TITLE_KEYWORDS = ["frontend", "front-end", "react", "next.js", "vue", "javascript", "web", "software", "ui", "ux"]

# Default Search Profiles for Remote Frontend Jobs
TARGET_PROFILES = [
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Next.js") NOT ("Backend" OR "Fullstack" OR "Full-stack")',
        "location": "Egypt",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Next.js") NOT ("Backend" OR "Fullstack" OR "Full-stack")',
        "location": "Saudi Arabia",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Next.js") NOT ("Backend" OR "Fullstack" OR "Full-stack")',
        "location": "United Arab Emirates",
    }
]

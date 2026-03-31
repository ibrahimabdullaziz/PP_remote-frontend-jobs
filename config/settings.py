import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
DATABASE_PATH = "data/state.db"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Scraper Settings
POLL_INTERVAL_SECONDS = 300 # 5 minutes

# Default Search Profiles for Remote Frontend Jobs
TARGET_PROFILES = [
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Vue") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "Worldwide",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Vue") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "Egypt",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Vue") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "Saudi Arabia",
    },
    {
        "keywords": '("Frontend" OR "Front-end" OR "React" OR "Vue") AND ("Junior" OR "Intern" OR "Mid")',
        "location": "United Arab Emirates",
    }
]

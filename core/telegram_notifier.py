import telegram
from telegram.constants import ParseMode
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, ADMIN_CHAT_ID

# Initialize bot only if token is provided
if TELEGRAM_TOKEN and TELEGRAM_TOKEN != "YOUR_TELEGRAM_TOKEN_HERE":
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
else:
    bot = None

async def send_admin_alert(message: str):
    if not bot or not ADMIN_CHAT_ID:
        print(f"[Admin Alert Mock] {message}")
        return
    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"⚠️ <b>Bot Alert</b>\n\n{message}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        print(f"Failed to send admin alert: {e}")

async def send_job_alert(job: dict):
    if not bot:
        print(f"[Mock Telegram Alert] New Job: {job['title']} at {job['company']}")
        return
        
    message = (
        f"🏢 <b>Company:</b> {job['company']}\n\n"
        f"💼 <b>Role:</b> {job['title']}\n\n"
        f"📍 <b>Location:</b> {job['location']}\n\n"
        f"⏱ <b>Posted:</b> {job.get('time_posted', 'Recently')}\n\n"
        f"🔗 <a href='{job['url']}'>Apply Here</a>"
    )
    
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Telegram API Error: {e}")

import os
import time
import requests
import random
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Try to load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.warning("TELEGRAM_BOT_TOKEN environment variable not set. Please set it to run the bot.")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# List of trading quotes (English and Russian)
QUOTES = [
    "The trend is your friend. / Тренд - твой друг.",
    "Cut your losses short and let your winners run. / Режь убытки, давай прибыли течь.",
    "Risk comes from not knowing what you're doing. - Warren Buffett / Риск происходит от незнания того, что ты делаешь.",
    "Markets can remain irrational longer than you can remain solvent. - Keynes / Рынки могут оставаться иррациональными дольше, чем вы сможете оставаться платежеспособным.",
    "Plan your trade and trade your plan. / Планируй сделку и торгуй по плану.",
    "Buy the rumor, sell the news. / Покупай на слухах, продавай на новостях.",
    "Opportunities come infrequently. When it rains gold, put out the bucket, not the thimble. - Warren Buffett",
    "The goal of a successful trader is to make the best trades. Money is secondary. - Alexander Elder"
]

def get_updates(offset=None):
    """Fetch updates from Telegram API"""
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting updates: {e}")
        return None

def send_message(chat_id, text):
    """Send a text message to a specific chat ID"""
    url = f"{BASE_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message: {e}")
        return False

def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN is missing.")
        return

    logger.info("Bot started...")
    offset = None
    
    while True:
        updates = get_updates(offset)
        
        if updates and "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                
                # Check for message or channel_post
                msg = update.get("message") or update.get("channel_post")
                
                if msg and "text" in msg:
                    text = msg.get("text", "")
                    chat_id = msg["chat"]["id"]
                    
                    if text.strip().startswith("/start"):
                        logger.info(f"Received /start from {chat_id}")
                        quote = random.choice(QUOTES)
                        send_message(chat_id, quote)
        
        time.sleep(1)

if __name__ == "__main__":
    main()

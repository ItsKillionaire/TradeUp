import telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import logging

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        logger.info("TelegramService initialized.")

    async def send_message(self, message):
        try:
            await self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            logger.info(f"Telegram message sent: {message}")
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")

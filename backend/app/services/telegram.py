import telegram
from config import settings
import logging

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self):
        if settings.TELEGRAM_BOT_TOKEN:
            self.bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
            logger.info("TelegramService initialized.")
        else:
            self.bot = None
            logger.warning(
                "TelegramService not initialized because TELEGRAM_BOT_TOKEN is not set."
            )

    async def send_message(self, message):
        if self.bot and settings.TELEGRAM_CHAT_ID:
            try:
                await self.bot.send_message(
                    chat_id=settings.TELEGRAM_CHAT_ID, text=message
                )
                logger.info(f"Telegram message sent: {message}")
            except Exception as e:
                logger.error(f"Error sending Telegram message: {e}")
        elif not self.bot:
            logger.warning(
                f"Telegram message not sent because bot is not initialized: {message}"
            )
        else:
            logger.warning(
                f"Telegram message not sent because TELEGRAM_CHAT_ID is not set: {message}"
            )

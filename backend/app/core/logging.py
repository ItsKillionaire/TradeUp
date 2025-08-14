import logging
import sys
from app.core.websocket_logging_handler import WebSocketLoggingHandler


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("trading_bot.log"),
            WebSocketLoggingHandler(),
        ],
    )

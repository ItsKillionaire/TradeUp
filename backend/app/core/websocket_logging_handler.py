import logging
from app.core.connection_manager import manager
import asyncio

class WebSocketLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(manager.broadcast_json({"type": "log", "message": log_entry}))

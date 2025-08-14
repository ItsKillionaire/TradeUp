import logging
from app.core.queue import message_queue

class WebSocketLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        message_queue.put({"type": "log", "message": log_entry})

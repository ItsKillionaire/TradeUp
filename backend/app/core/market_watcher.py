import asyncio
import logging
from app.services.alpaca import AlpacaService
from app.core.connection_manager import manager

logger = logging.getLogger(__name__)

async def watch_market_status():
    alpaca_service = AlpacaService()
    while True:
        try:
            clock = alpaca_service.get_clock()
            await manager.broadcast_json({
                "type": "market_status_update",
                "data": {
                    "is_open": clock.is_open,
                    "next_open": clock.next_open.isoformat(),
                    "next_close": clock.next_close.isoformat(),
                    "timestamp": clock.timestamp.isoformat()
                }
            })
        except Exception as e:
            logger.error(f"Error fetching market status: {e}")
        await asyncio.sleep(60)

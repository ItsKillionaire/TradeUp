from sqlalchemy.orm import Session
from app.models.trade import Trade
from datetime import datetime
import logging
from app.core.connection_manager import manager

logger = logging.getLogger(__name__)

async def create_trade(db: Session, symbol: str, qty: float, price: float, side: str, strategy: str, entry_reason: str, exit_reason: str = None):
    logger.info(f"Attempting to create trade: Symbol={symbol}, Qty={qty}, Price={price}, Side={side}")
    db_trade = Trade(
        symbol=symbol,
        qty=qty,
        price=price,
        side=side,
        timestamp=datetime.utcnow(),
        strategy=strategy,
        entry_reason=entry_reason,
        exit_reason=exit_reason
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    logger.info(f"Trade created: {db_trade.id}")
    await manager.broadcast_json({{"type": "trades_update", "data": db_trade.to_dict()}})
    return db_trade

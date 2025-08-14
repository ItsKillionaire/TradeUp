from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    qty = Column(Float)
    price = Column(Float)
    side = Column(String)
    timestamp = Column(DateTime)
    strategy = Column(String, nullable=True)
    entry_reason = Column(String, nullable=True)
    exit_reason = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "qty": self.qty,
            "price": self.price,
            "side": self.side,
            "timestamp": self.timestamp.isoformat(),
            "strategy": self.strategy,
            "entry_reason": self.entry_reason,
            "exit_reason": self.exit_reason,
        }

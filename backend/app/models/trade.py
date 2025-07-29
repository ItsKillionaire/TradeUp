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

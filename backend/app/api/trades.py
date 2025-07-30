from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.trade import Trade
from app.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/trades")
def get_trades(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    trades = db.query(Trade).all()
    return trades

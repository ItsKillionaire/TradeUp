from fastapi import APIRouter, Depends
from app.services.alpaca import AlpacaService

router = APIRouter()


@router.get("/status")
def get_market_status():
    alpaca_service = AlpacaService()
    clock = alpaca_service.get_clock()
    return {
        "is_open": clock.is_open,
        "next_open": clock.next_open.isoformat(),
        "next_close": clock.next_close.isoformat(),
        "timestamp": clock.timestamp.isoformat(),
    }

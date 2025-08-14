from fastapi import APIRouter, Depends
from app.services.market_scanner import MarketScanner
from app.services.alpaca import AlpacaService, get_alpaca_service

router = APIRouter()


@router.post("/scan")
def run_market_scan(alpaca_service: AlpacaService = Depends(get_alpaca_service)):
    scanner = MarketScanner(alpaca_service)
    promising_symbols = scanner.run_scan()
    return {"promising_symbols": promising_symbols}

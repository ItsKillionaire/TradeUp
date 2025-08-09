
from fastapi import APIRouter, Depends
from ..backtester.backtester import Backtester
from ..services.alpaca import get_alpaca_service
from ..strategies.base import get_strategy

print("Backtester router imported")

router = APIRouter()

@router.post("/backtest")
def run_backtest(symbol: str, strategy_name: str, start_date: str, end_date: str, alpaca_service = Depends(get_alpaca_service)):
    strategy = get_strategy(strategy_name)
    if not strategy:
        return {"error": f"Strategy '{strategy_name}' not found."}

    backtester = Backtester(alpaca_service, strategy, start_date, end_date)
    results = backtester.run(symbol)
    return results

from fastapi import APIRouter, Depends
from app.services.alpaca import AlpacaService
from app.core.scheduler import scheduler
from app.core.strategy_manager import StrategyManager

router = APIRouter()

def get_alpaca_service():
    return AlpacaService()

@router.post("/strategy/start/{strategy_name}/{symbol}")
async def start_strategy(strategy_name: str, symbol: str, alpaca_service: AlpacaService = Depends(get_alpaca_service)):
    strategy_manager = StrategyManager(alpaca_service)
    strategy = strategy_manager.get_strategy(strategy_name)
    if strategy:
        scheduler.add_job(strategy.run, 'interval', minutes=1, args=[symbol, "1Min"], id=f"{strategy_name}_{symbol}", replace_existing=True)
        if not scheduler.running:
            scheduler.start()
        return {"message": f"Strategy {strategy_name} started for {symbol}"}
    return {"message": f"Strategy {strategy_name} not found"}

@router.post("/strategy/stop/{strategy_name}/{symbol}")
async def stop_strategy(strategy_name: str, symbol: str):
    job_id = f"{strategy_name}_{symbol}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        await telegram_service.send_message(f"Strategy {strategy_name} stopped for {symbol}")
        return {"message": f"Strategy {strategy_name} stopped for {symbol}"}
    return {"message": f"Strategy {strategy_name} not running for {symbol}"}

@router.get("/strategy/status")
def get_strategy_status():
    return {"status": "online" if scheduler.running else "offline"}

@router.get("/strategy/available")
def get_available_strategies(alpaca_service: AlpacaService = Depends(get_alpaca_service)):
    strategy_manager = StrategyManager(alpaca_service)
    return {"strategies": strategy_manager.get_available_strategies()}

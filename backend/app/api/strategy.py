from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.alpaca import AlpacaService
from app.core.scheduler import scheduler
from app.core.strategy_manager import StrategyManager
from app.services.telegram import TelegramService
from app.dependencies import get_current_user
from app.core.database import get_db

router = APIRouter()

def get_alpaca_service():
    return AlpacaService()

def get_telegram_service():
    return TelegramService()

@router.post("/strategy/start/{strategy_name}/{symbol}")
async def start_strategy(
    strategy_name: str,
    symbol: str,
    trade_percentage: float = 0.05, # New parameter
    alpaca_service: AlpacaService = Depends(get_alpaca_service),
    telegram_service: TelegramService = Depends(get_telegram_service),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    strategy_manager = StrategyManager(alpaca_service)
    try:
        scheduler.add_job(
            strategy_manager.run_strategy,
            'interval',
            minutes=1,
            args=[strategy_name, symbol, "1Min", db, {"trade_percentage": trade_percentage}], # Pass db session and strategy params
            id=f"{strategy_name}_{symbol}",
            replace_existing=True
        )
        if not scheduler.running:
            scheduler.start()
        await telegram_service.send_message(f"Strategy {strategy_name} started for {symbol}")
        return {"message": f"Strategy {strategy_name} started for {symbol}"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/strategy/stop/{strategy_name}/{symbol}")
async def stop_strategy(
    strategy_name: str,
    symbol: str,
    telegram_service: TelegramService = Depends(get_telegram_service),
    current_user: dict = Depends(get_current_user)
):
    job_id = f"{strategy_name}_{symbol}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        await telegram_service.send_message(f"Strategy {strategy_name} stopped for {symbol}")
        return {"message": f"Strategy {strategy_name} stopped for {symbol}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Strategy {strategy_name} not running for {symbol}")

@router.get("/strategy/status")
def get_strategy_status(current_user: dict = Depends(get_current_user)):
    return {"status": "online" if scheduler.running else "offline"}

@router.get("/strategy/available")
def get_available_strategies(alpaca_service: AlpacaService = Depends(get_alpaca_service), current_user: dict = Depends(get_current_user)):
    strategy_manager = StrategyManager(alpaca_service)
    return {"strategies": strategy_manager.get_available_strategies()}

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.services.alpaca import AlpacaService
from app.core.strategy_manager import StrategyManager
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService
from app.core.database import get_db

router = APIRouter()


def get_alpaca_service():
    return AlpacaService()


def get_telegram_service():
    return TelegramService()


def get_google_sheets_service():
    return GoogleSheetsService()


@router.post("/strategy/start/{strategy_name}/{symbol}")
async def start_strategy(
    request: Request,
    strategy_name: str,
    symbol: str,
    strategy_params: dict = {},
    db: Session = Depends(get_db),
):
    strategy_manager = request.app.state.strategy_manager
    try:
        strategy_instance = strategy_manager.get_strategy_instance(
            strategy_name, **strategy_params
        )
        strategy_manager.active_strategies.append(strategy_instance)
        await strategy_manager.telegram_service.send_message(
            f"Strategy {strategy_name} started for {symbol}"
        )
        return {"message": f"Strategy {strategy_name} started for {symbol}"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/strategy/stop/{strategy_name}/{symbol}")
async def stop_strategy(
    request: Request,
    strategy_name: str,
    symbol: str,
):
    strategy_manager = request.app.state.strategy_manager
    strategy_manager.active_strategies = [
        s
        for s in strategy_manager.active_strategies
        if not (s.name == strategy_name and s.symbol == symbol)
    ]
    await strategy_manager.telegram_service.send_message(
        f"Strategy {strategy_name} stopped for {symbol}"
    )
    return {"message": f"Strategy {strategy_name} stopped for {symbol}"}


@router.get("/strategy/status")
def get_strategy_status():
    return {"message": "Strategy manager is online"}


from app.strategies.base import get_strategy


@router.post("/strategy/ai/train")
def train_ai_strategy(symbol: str, start_date: str = None, end_date: str = None):
    ai_strategy = get_strategy("AI Strategy")
    if not ai_strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="AI Strategy not found."
        )

    result = ai_strategy.train(symbol, start_date=start_date, end_date=end_date)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["error"]
        )

    return {"data": result}


@router.get("/strategy/available")
def get_available_strategies(request: Request):
    strategy_manager = request.app.state.strategy_manager
    return {"data": {"strategies": strategy_manager.get_available_strategies()}}

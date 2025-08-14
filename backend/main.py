import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import account, strategy, google_sheets, websocket, trades, market, scanner
from app.core.logging import setup_logging
from app.core.database import engine
from app.models import trade
import asyncio
from app.services.alpaca import AlpacaService
from app.core.connection_manager import manager
from app.core.strategy_manager import StrategyManager
from app.core.risk_manager import RiskManager
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService
from app.core.market_watcher import watch_market_status

trade.Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI()

alpaca_service = AlpacaService()


async def broadcast_updates():
    while True:
        try:
            positions = alpaca_service.get_open_positions()
            orders = alpaca_service.get_orders()
            await manager.broadcast_json(
                {"type": "positions_update", "data": positions}
            )
            await manager.broadcast_json({"type": "orders_update", "data": orders})
        except Exception as e:
            logging.error(f"Error broadcasting updates: {e}")
        await asyncio.sleep(5)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_updates())
    asyncio.create_task(watch_market_status())
    account_info = await alpaca_service.get_account_info()
    risk_manager = RiskManager(account_equity=float(account_info["equity"]))
    telegram_service = TelegramService()
    google_sheets_service = GoogleSheetsService()
    app.state.strategy_manager = StrategyManager(
        alpaca_service, risk_manager, telegram_service, google_sheets_service
    )
    await alpaca_service.start_stream(app.state.strategy_manager)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router, prefix="/api")
app.include_router(strategy.router, prefix="/api")
app.include_router(google_sheets.router, prefix="/api")
app.include_router(websocket.router)
app.include_router(trades.router, prefix="/api")
app.include_router(market.router, prefix="/api/market")
app.include_router(scanner.router, prefix="/api/scanner")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
def read_root():
    return {"message": "Alpaca Trader Bot API"}

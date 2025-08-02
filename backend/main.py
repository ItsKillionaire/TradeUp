from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import account, strategy, google_sheets, websocket, trades
from app.core.logging import setup_logging
from app.core.database import engine
from app.models import trade

setup_logging()

trade.Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router, prefix="/api")
app.include_router(strategy.router, prefix="/api")
app.include_router(google_sheets.router, prefix="/api")
app.include_router(websocket.router)
app.include_router(trades.router, prefix="/api")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.get("/")
def read_root():
    return {"message": "Alpaca Trader Bot API"}

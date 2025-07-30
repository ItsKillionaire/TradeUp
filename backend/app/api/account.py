from fastapi import APIRouter, Depends
from app.services.alpaca import AlpacaService
from app.dependencies import get_current_user

router = APIRouter()

def get_alpaca_service():
    return AlpacaService()

@router.get("/account")
async def get_account(alpaca_service: AlpacaService = Depends(get_alpaca_service), current_user: dict = Depends(get_current_user)):
    return await alpaca_service.get_account_info()

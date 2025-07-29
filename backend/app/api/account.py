from fastapi import APIRouter, Depends
from app.services.alpaca import AlpacaService

router = APIRouter()

def get_alpaca_service():
    return AlpacaService()

@router.get("/account")
def get_account(alpaca_service: AlpacaService = Depends(get_alpaca_service)):
    return alpaca_service.get_account_info()

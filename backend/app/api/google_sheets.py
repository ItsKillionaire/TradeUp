from fastapi import APIRouter
from app.services.google_sheets import GoogleSheetsService

router = APIRouter()

@router.post("/export/google-sheets")
def export_to_google_sheets():
    service = GoogleSheetsService()
    service.export_trades()
    return {"message": "Trades exported to Google Sheets successfully"}

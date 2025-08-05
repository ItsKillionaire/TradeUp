import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.core.database import SessionLocal
from app.models.trade import Trade
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('/home/killionaire/secrets/google_creds.json', scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open("Trading_log").sheet1
        logger.info("GoogleSheetsService initialized.")

    def export_trades(self):
        try:
            db = SessionLocal()
            trade = db.query(Trade).order_by(Trade.id.desc()).first()
            db.close()

            if not trade:
                logger.info("No trades to export.")
                return

            # Check if header exists
            header = self.sheet.row_values(1)
            if not header or header != ["ID", "Symbol", "Quantity", "Price", "Side", "Timestamp", "Strategy", "Entry Reason", "Exit Reason"]:
                self.sheet.clear()
                self.sheet.append_row(["ID", "Symbol", "Quantity", "Price", "Side", "Timestamp", "Strategy", "Entry Reason", "Exit Reason"])

            row = [trade.id, trade.symbol, trade.qty, trade.price, trade.side, str(trade.timestamp), trade.strategy, trade.entry_reason, trade.exit_reason]
            self.sheet.append_row(row)
            logger.info(f"Exported trade {trade.id} to Google Sheets.")
        except Exception as e:
            logger.error(f"Error exporting trades to Google Sheets: {e}")

    def backfill_trades(self):
        try:
            db = SessionLocal()
            trades = db.query(Trade).all()
            db.close()

            self.sheet.clear()
            header = ["ID", "Symbol", "Quantity", "Price", "Side", "Timestamp", "Strategy", "Entry Reason", "Exit Reason"]
            self.sheet.append_row(header)

            for trade in trades:
                row = [trade.id, trade.symbol, trade.qty, trade.price, trade.side, str(trade.timestamp), trade.strategy, trade.entry_reason, trade.exit_reason]
                self.sheet.append_row(row)
            logger.info(f"Backfilled {len(trades)} trades to Google Sheets.")
        except Exception as e:
            logger.error(f"Error backfilling trades to Google Sheets: {e}")

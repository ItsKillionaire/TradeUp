import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.database import SessionLocal, engine, Base
from app.models.trade import Trade
from app.services.alpaca import AlpacaService
from app.services.google_sheets import GoogleSheetsService
from app.crud import create_trade
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def backfill_trades_from_alpaca():
    db = SessionLocal()
    alpaca_service = AlpacaService()
    google_sheets_service = GoogleSheetsService()

    try:
        # 1. Clear existing trades in the local database to avoid duplicates
        logger.info("Clearing existing trades from the database...")
        db.query(Trade).delete()
        db.commit()

        # 2. Fetch closed orders from Alpaca
        logger.info("Fetching historical orders from Alpaca...")
        orders = alpaca_service.api.list_orders(status='closed', limit=500, direction='asc')
        filled_orders = [o for o in orders if o.filled_at is not None]
        logger.info(f"Found {len(filled_orders)} filled historical orders.")

        # 3. Populate the local database
        for order in filled_orders:
            create_trade(
                db,
                symbol=order.symbol,
                qty=float(order.filled_qty),
                price=float(order.filled_avg_price),
                side=order.side,
                strategy="Historical Import",
                entry_reason=f"Imported from Alpaca order {order.id}",
                exit_reason=None
            )
        logger.info("Successfully populated the local database with historical trades.")

        # 4. Export all trades from DB to Google Sheets
        logger.info("Starting backfill to Google Sheets...")
        google_sheets_service.backfill_trades()
        logger.info("Google Sheets backfill completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during the backfill process: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    backfill_trades_from_alpaca()

import logging
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService
from app.crud import create_trade
from app.core.connection_manager import manager
from sqlalchemy.orm import Session


class SmaCrossover(BaseStrategy):
    def __init__(
        self,
        alpaca_service,
        risk_manager,
        telegram_service,
        google_sheets_service,
        short_window=40,
        long_window=100,
        trade_percentage=0.05,
        take_profit_pct=0.05,
        stop_loss_pct=0.02,
    ):
        super().__init__(alpaca_service, risk_manager, "SMA Crossover")
        self.short_window = short_window
        self.long_window = long_window
        self.take_profit_pct = take_profit_pct
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service

    def generate_signals(self, bars):
        if len(bars) < self.long_window:
            logging.warning(
                f"Not enough data to generate signals. Need {self.long_window}, have {len(bars)}."
            )
            signals = pd.DataFrame(index=bars.index)
            signals["signal"] = 0
            signals["position"] = 0
            return signals

        signals = pd.DataFrame(index=bars.index)
        signals["short_mavg"] = (
            bars["close"].rolling(self.short_window, min_periods=1).mean()
        )
        signals["long_mavg"] = (
            bars["close"].rolling(self.long_window, min_periods=1).mean()
        )

        signals["signal"] = 0
        signals.loc[signals.index[self.short_window :], "signal"] = np.where(
            signals["short_mavg"][self.short_window :]
            > signals["long_mavg"][self.short_window :],
            1,
            0,
        )

        signals["position"] = signals["signal"].diff()
        return signals

    async def run(self, symbol, timeframe, db: Session):
        logging.info(
            f"Running SMA Crossover strategy for {symbol} with Risk Management"
        )

        bars_data = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.long_window + 20
        )
        if not bars_data or len(bars_data.df) < self.long_window:
            logging.warning(f"Not enough data for {symbol} to run strategy.")
            return

        bars = bars_data.df
        signals = self.generate_signals(bars)
        latest_position = signals["position"].iloc[-1]
        current_position_qty = await self.get_position(symbol)

        if latest_position == 1.0 and current_position_qty == 0:
            last_price = bars["close"].iloc[-1]

            atr = self.risk_manager.calculate_atr(bars)
            stop_loss_price = self.risk_manager.calculate_stop_loss(
                last_price, atr.iloc[-1]
            )

            qty_to_buy = self.risk_manager.calculate_position_size(
                last_price, stop_loss_price
            )

            if qty_to_buy > 0:
                take_profit_price = last_price + (last_price - stop_loss_price) * 2

                message = (
                    f"TRADE SIGNAL: Buy {symbol}.\n"
                    f"Reason: SMA Crossover with Risk Management.\n"
                    f"  - Position Size: {qty_to_buy:.4f} shares\n"
                    f"  - Entry Price: ${last_price:,.2f}\n"
                    f"  - Stop Loss: ${stop_loss_price:,.2f}\n"
                    f"  - Take Profit: ${take_profit_price:,.2f}"
                )
                logging.info(message)
                await self.telegram_service.send_message(message)
                await manager.broadcast_json({"type": "log", "message": message})

                order = self.alpaca_service.submit_order(
                    symbol=symbol,
                    qty=qty_to_buy,
                    side="buy",
                    type="market",
                    time_in_force="day",
                    order_class="bracket",
                    take_profit={"limit_price": round(take_profit_price, 2)},
                    stop_loss={"stop_price": round(stop_loss_price, 2)},
                )
                create_trade(
                    db,
                    symbol=symbol,
                    qty=order.qty or 0,
                    price=order.filled_avg_price or last_price,
                    side=order.side,
                    strategy=self.name,
                    entry_reason="SMA Crossover Signal",
                )
                self.google_sheets_service.export_trades()

        elif latest_position == -1.0 and current_position_qty > 0:
            message = f"TRADE SIGNAL: Sell {symbol}. Reason: SMA Crossover exit signal. Closing position."
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})

            self.alpaca_service.api.close_position(symbol)
            create_trade(
                db,
                symbol=symbol,
                qty=current_position_qty,
                price=bars["close"].iloc[-1],
                side="sell",
                strategy=self.name,
                exit_reason="SMA Crossover Exit Signal",
            )
            self.google_sheets_service.export_trades()
        else:
            logging.info(
                f"No new signal for {symbol} or position is aligned with signal."
            )

    async def get_position(self, symbol):
        try:
            position = self.alpaca_service.api.get_position(symbol)
            return float(position.qty)
        except Exception as e:
            return 0

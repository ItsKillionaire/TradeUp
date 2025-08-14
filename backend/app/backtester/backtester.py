import logging
import pandas as pd
import numpy as np
from datetime import datetime

from ..core.risk_manager import RiskManager


class Backtester:
    def __init__(
        self, alpaca_service, strategy, start_date, end_date, initial_capital=100000
    ):
        self.alpaca_service = alpaca_service
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.portfolio_value = initial_capital
        self.positions = {}
        self.trades = []
        self.risk_manager = RiskManager(account_equity=self.initial_capital)

    def run(self, symbol, timeframe="1Day"):
        logging.info(
            f"Starting backtest for {symbol} from {self.start_date} to {self.end_date} with Risk Management"
        )

        try:
            bars_data = self.alpaca_service.get_bars(
                symbol=symbol,
                timeframe=timeframe,
                start=self.start_date,
                end=self.end_date,
            )
            if not bars_data or bars_data.df.empty:
                logging.warning(f"No data found for {symbol} in the given date range.")
                return {"error": "No data found."}
            bars = bars_data.df
        except Exception as e:
            logging.error(f"Error fetching bars for backtest: {e}")
            return {"error": str(e)}

        signals = self.strategy.generate_signals(bars)
        atr = self.risk_manager.calculate_atr(bars)

        for i in range(len(bars)):
            current_price = bars["close"].iloc[i]
            date = bars.index[i]
            self._update_portfolio_value(current_price, symbol)

            signal = signals["position"].iloc[i]

            if (
                signal == 1.0 and self.positions.get(symbol, 0) == 0
            ):  # Buy Signal and no position
                stop_loss_price = self.risk_manager.calculate_stop_loss(
                    current_price, atr.iloc[i]
                )
                qty_to_buy = self.risk_manager.calculate_position_size(
                    current_price, stop_loss_price
                )
                self._execute_buy(symbol, current_price, date, qty_to_buy)

            elif (
                signal == -1.0 and self.positions.get(symbol, 0) > 0
            ):  # Sell Signal and in position
                self._execute_sell(symbol, current_price, date)

        return self._calculate_performance(bars)

    def _update_portfolio_value(self, current_price, symbol):
        position_value = self.positions.get(symbol, 0) * current_price
        self.portfolio_value = self.cash + position_value

    def _execute_buy(self, symbol, price, date, qty_to_buy):
        if self.cash > 0 and qty_to_buy > 0:
            cost = qty_to_buy * price
            if self.cash >= cost:
                self.positions[symbol] = self.positions.get(symbol, 0) + qty_to_buy
                self.cash -= cost
                self.trades.append(
                    {
                        "date": date,
                        "symbol": symbol,
                        "side": "buy",
                        "qty": qty_to_buy,
                        "price": price,
                    }
                )
                logging.debug(f"{date}: Bought {qty_to_buy} of {symbol} at {price}")

    def _execute_sell(self, symbol, price, date):
        if self.positions.get(symbol, 0) > 0:
            qty_to_sell = self.positions[symbol]
            self.cash += qty_to_sell * price
            self.positions[symbol] = 0
            self.trades.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "side": "sell",
                    "qty": qty_to_sell,
                    "price": price,
                }
            )
            logging.debug(f"{date}: Sold {qty_to_sell} of {symbol} at {price}")

    def _calculate_performance(self, bars):
        if not self.trades:
            return {
                "message": "No trades were executed.",
                "initial_capital": self.initial_capital,
                "final_portfolio_value": self.portfolio_value,
                "net_profit": 0,
                "return_pct": 0,
                "trades": [],
            }

        final_value = self.portfolio_value
        net_profit = final_value - self.initial_capital
        return_pct = (net_profit / self.initial_capital) * 100

        return {
            "initial_capital": self.initial_capital,
            "final_portfolio_value": round(final_value, 2),
            "net_profit": round(net_profit, 2),
            "return_pct": round(return_pct, 2),
            "total_trades": len(self.trades),
            "trades": self.trades,
        }

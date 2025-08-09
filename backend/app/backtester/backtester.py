import pandas as pd
from typing import List, Dict, Any
from ..services.alpaca import AlpacaService
from ..strategies.base import BaseStrategy

class Backtester:
    def __init__(self, alpaca_service: AlpacaService, strategy: BaseStrategy, start_date: str, end_date: str, initial_capital=100000):
        self.alpaca_service = alpaca_service
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.portfolio_value = initial_capital

    def run(self, symbol: str) -> Dict[str, Any]:
        """
        Runs the backtest for a given symbol.
        """
        historical_data = self.alpaca_service.get_historical_data(symbol, self.start_date, self.end_date)
        if historical_data.empty:
            return {"error": "No historical data found for the given symbol and date range."}

        signals = self.strategy.generate_signals(historical_data)
        trades = self._simulate_trades(historical_data, signals)
        performance = self._calculate_performance(trades)

        return {
            "symbol": symbol,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "strategy": self.strategy.name,
            "performance": performance,
            "trades": trades
        }

    def _simulate_trades(self, historical_data: pd.DataFrame, signals: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Simulates trades based on the strategy signals.
        """
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        portfolio = pd.DataFrame(index=signals.index).fillna(0.0)

        positions[historical_data['symbol'][0]] = 100 * signals['signal']   # This is a simplified position sizing
        portfolio['positions'] = (positions.multiply(historical_data['close'], axis=0))
        portfolio['cash'] = self.initial_capital - (positions.diff().multiply(historical_data['close'], axis=0)).cumsum()
        portfolio['total'] = portfolio['cash'] + portfolio['positions']
        
        trades = []
        for i in range(len(signals)):
            if signals['positions'].iloc[i] != 0:
                trade = {
                    "date": signals.index[i],
                    "symbol": historical_data['symbol'][0],
                    "action": "buy" if signals['positions'].iloc[i] > 0 else "sell",
                    "quantity": abs(signals['positions'].iloc[i] * 100), # Simplified quantity
                    "price": historical_data['close'].iloc[i]
                }
                trades.append(trade)

        return trades

    def _calculate_performance(self, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates performance metrics from the trades.
        """
        if not trades:
            return {}

        total_profit_loss = 0
        for trade in trades:
            if trade['action'] == 'buy':
                total_profit_loss -= trade['quantity'] * trade['price']
            else:
                total_profit_loss += trade['quantity'] * trade['price']

        return {
            "total_profit_loss": total_profit_loss
        }
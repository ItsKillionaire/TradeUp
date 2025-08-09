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
        trades, portfolio_values = self._simulate_trades(historical_data, signals)
        performance = self._calculate_performance(trades, portfolio_values)

        return {
            "symbol": symbol,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "strategy": self.strategy.name,
            "performance": performance,
            "trades": trades
        }

    def _simulate_trades(self, historical_data: pd.DataFrame, signals: pd.DataFrame) -> tuple[List[Dict[str, Any]], pd.Series]:
        """
        Simulates trades based on the strategy signals.
        """
        trades = []
        position = 0
        buy_price = 0
        portfolio_values = []
        cash = self.initial_capital

        for i in range(len(signals)):
            portfolio_value = cash
            if position == 1:
                portfolio_value += 100 * historical_data['close'].iloc[i]
            
            if signals['signal'].iloc[i] == 1 and position == 0: # Buy signal
                position = 1
                buy_price = historical_data['close'].iloc[i]
                cash -= 100 * buy_price
                trades.append({
                    "date": signals.index[i],
                    "symbol": historical_data['symbol'][0],
                    "action": "buy",
                    "quantity": 100,
                    "price": buy_price
                })
            elif signals['signal'].iloc[i] == -1 and position == 1: # Sell signal
                position = 0
                sell_price = historical_data['close'].iloc[i]
                cash += 100 * sell_price
                trades.append({
                    "date": signals.index[i],
                    "symbol": historical_data['symbol'][0],
                    "action": "sell",
                    "quantity": 100,
                    "price": sell_price
                })
            portfolio_values.append(portfolio_value)

        return trades, pd.Series(portfolio_values, index=signals.index)

    def _calculate_performance(self, trades: List[Dict[str, Any]], portfolio_values: pd.Series) -> Dict[str, Any]:
        """
        Calculates performance metrics from the trades.
        """
        if not trades or len(trades) % 2 != 0:
            return {}

        total_profit_loss = 0
        wins = 0
        losses = 0
        for i in range(0, len(trades), 2):
            buy_trade = trades[i]
            sell_trade = trades[i+1]
            profit_loss = (sell_trade['price'] - buy_trade['price']) * buy_trade['quantity']
            total_profit_loss += profit_loss
            if profit_loss > 0:
                wins += 1
            else:
                losses += 1
        
        win_rate = wins / (wins + losses) if (wins + losses) > 0 else 0

        # Max Drawdown
        peak = portfolio_values.cummax()
        drawdown = (portfolio_values - peak) / peak
        max_drawdown = drawdown.min()

        # Sharpe Ratio
        returns = portfolio_values.pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std()) * (252**0.5) # Annualized

        return {
            "total_profit_loss": total_profit_loss,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio
        }
import logging
import pandas as pd
import numpy as np


class RiskManager:
    def __init__(self, account_equity):
        if account_equity <= 0:
            raise ValueError("Account equity must be positive.")
        self.account_equity = account_equity
        logging.info(
            f"RiskManager initialized with account equity of: ${self.account_equity:,.2f}"
        )

    def calculate_position_size(
        self, entry_price, stop_loss_price, risk_percentage=0.01
    ):
        """
        Calculates the number of shares to trade based on a fixed fractional risk model.

        :param entry_price: The price at which the asset is to be bought.
        :param stop_loss_price: The price at which the position will be sold for a loss.
        :param risk_percentage: The percentage of account equity to risk on this trade.
        :return: The number of shares to trade. Returns 0 if risk is invalid.
        """
        if entry_price <= 0 or stop_loss_price <= 0:
            logging.warning("Entry price and stop loss price must be positive.")
            return 0

        risk_per_share = entry_price - stop_loss_price
        if risk_per_share <= 0:
            logging.warning(
                "Stop loss price must be less than the entry price for a long position."
            )
            return 0

        capital_to_risk = self.account_equity * risk_percentage
        position_size = capital_to_risk / risk_per_share

        logging.info(
            f"Position size calculated: {position_size:.4f} shares. (Risking ${capital_to_risk:,.2f})"
        )
        return position_size

    def calculate_atr(self, bars: pd.DataFrame, period=14) -> pd.Series:
        """Calculates the Average True Range (ATR)."""
        if len(bars) < period:
            return pd.Series(index=bars.index, dtype=float)

        high_low = bars["high"] - bars["low"]
        high_close = np.abs(bars["high"] - bars["close"].shift())
        low_close = np.abs(bars["low"] - bars["close"].shift())

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr

    def calculate_stop_loss(self, entry_price, atr_value, atr_multiplier=2.0):
        if atr_value is None or np.isnan(atr_value) or atr_value <= 0:
            logging.warning("Invalid ATR value, cannot calculate dynamic stop loss.")
            # Fallback to a fixed percentage if ATR is not available
            return entry_price * 0.98  # Default 2% stop loss

        stop_loss_price = entry_price - (atr_value * atr_multiplier)
        logging.info(
            f"Calculated dynamic stop loss at: ${stop_loss_price:,.2f} (Entry: ${entry_price:,.2f}, ATR: {atr_value:,.2f}) "
        )
        return stop_loss_price

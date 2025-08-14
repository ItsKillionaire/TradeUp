import logging
import pandas as pd
from alpaca_trade_api.rest import REST
from app.services.alpaca import AlpacaService


class MarketScanner:
    def __init__(self, alpaca_service: AlpacaService):
        self.api = alpaca_service.api
        self.data_api = alpaca_service.data_api
        self.alpaca_service = alpaca_service

    def get_tradable_assets(self):
        """Fetches a list of tradable, shortable, US equity assets."""
        try:
            assets = self.api.list_assets(status="active", asset_class="us_equity")
            tradable_assets = [a for a in assets if a.tradable and a.shortable]
            logging.info(f"Found {len(tradable_assets)} tradable US equity assets.")
            return [a.symbol for a in tradable_assets]
        except Exception as e:
            logging.error(f"Error fetching tradable assets: {e}")
            return []

    def scan(self, symbols, min_price=10, min_avg_volume=1000000, atr_threshold=0.03):
        """
        Scans a list of symbols based on technical criteria.

        :param symbols: A list of stock symbols to scan.
        :param min_price: Minimum price of the stock.
        :param min_avg_volume: Minimum average daily dollar volume.
        :param atr_threshold: Minimum ATR as a percentage of the price.
        :return: A list of symbols that meet the criteria.
        """
        promising_symbols = []
        total_symbols = len(symbols)
        logging.info(f"Scanning {total_symbols} symbols...")

        for i, symbol in enumerate(symbols):
            try:
                # Fetch daily bars for the last 30 days
                bars = self.alpaca_service.get_bars(symbol, "1Day", limit=30).df
                if len(bars) < 30:
                    continue

                last_price = bars["close"].iloc[-1]
                avg_volume = (bars["volume"] * bars["close"]).mean()

                # --- Apply Filters ---
                if last_price < min_price:
                    continue
                if avg_volume < min_avg_volume:
                    continue

                # ATR for volatility
                high_low = bars["high"] - bars["low"]
                high_close = abs(bars["high"] - bars["close"].shift())
                low_close = abs(bars["low"] - bars["close"].shift())
                tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                atr = tr.rolling(window=14).mean().iloc[-1]
                atr_pct = atr / last_price

                if atr_pct < atr_threshold:
                    continue

                # Trend filter (e.g., price > 20-day SMA)
                sma_20 = bars["close"].rolling(window=20).mean().iloc[-1]
                if last_price < sma_20:
                    continue

                logging.info(
                    f"[{(i+1)}/{total_symbols}] {symbol} is a promising candidate. Price: ${last_price:.2f}, Volatility: {atr_pct:.2%}"
                )
                promising_symbols.append(
                    {
                        "symbol": symbol,
                        "price": last_price,
                        "avg_volume": avg_volume,
                        "atr_pct": atr_pct,
                    }
                )

            except Exception as e:
                logging.debug(f"Could not process symbol {symbol}: {e}")
                continue

        logging.info(
            f"Scan complete. Found {len(promising_symbols)} promising symbols."
        )
        return promising_symbols

    def run_scan(self):
        tradable_symbols = self.get_tradable_assets()
        sample_symbols = tradable_symbols[:200]
        results = self.scan(sample_symbols)
        return results

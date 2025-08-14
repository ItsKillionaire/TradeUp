import os
import asyncio
import logging
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from app.strategies.base import BaseStrategy
import traceback

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MODEL_PATH = os.path.join(PROJECT_ROOT, "trained_models", "ai_strategy_model.joblib")


class AIStrategy(BaseStrategy):
    name: str = "ai_strategy"
    display_name: str = "AI Strategy"
    description: str = "A strategy that uses a trained AI model to generate trading signals."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self._load_model()

    def _load_model(self):
        try:
            model = joblib.load(MODEL_PATH)
            logging.info("AI model loaded successfully from disk.")
            return model
        except FileNotFoundError:
            logging.warning(
                "No pre-trained model found. The model needs to be trained."
            )
            return None

    def _save_model(self):
        if self.model:
            joblib.dump(self.model, MODEL_PATH)
            logging.info(f"AI model saved to {MODEL_PATH}")

    def _calculate_atr(self, bars: pd.DataFrame, period=14) -> pd.Series:
        """Calculates the Average True Range (ATR)."""
        if len(bars) < period:
            return pd.Series(index=bars.index, dtype=float)

        high_low = bars["high"] - bars["low"]
        high_close = np.abs(bars["high"] - bars["close"].shift())
        low_close = np.abs(bars["low"] - bars["close"].shift())

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr

    def _prepare_features(self, bars: pd.DataFrame) -> pd.DataFrame:
        """Creates a rich set of features for the model using pandas-ta."""
        try:
            import pandas_ta as ta

            features = pd.DataFrame(index=bars.index)
            
            # Momentum
            features['rsi'] = ta.rsi(bars.close)
            features['macd'] = ta.macd(bars.close).iloc[:, 0]
            features['macds'] = ta.macd(bars.close).iloc[:, 1]
            features['macdh'] = ta.macd(bars.close).iloc[:, 2]
            features['stoch_k'] = ta.stoch(bars.high, bars.low, bars.close).iloc[:, 0]
            features['stoch_d'] = ta.stoch(bars.high, bars.low, bars.close).iloc[:, 1]
            
            # Volatility
            features['bb_upper'] = ta.bbands(bars.close).iloc[:, 0]
            features['bb_mid'] = ta.bbands(bars.close).iloc[:, 1]
            features['bb_lower'] = ta.bbands(bars.close).iloc[:, 2]
            features['atr'] = ta.atr(bars.high, bars.low, bars.close)
            
            # Trend
            features['sma20'] = ta.sma(bars.close, length=20)
            features['sma50'] = ta.sma(bars.close, length=50)
            features['ema20'] = ta.ema(bars.close, length=20)
            features['ema50'] = ta.ema(bars.close, length=50)
            
            features.dropna(inplace=True)
            return features
        except ImportError:
            logging.error(
                "pandas-ta is not installed. Cannot create advanced features."
            )
            # Fallback to simple features
            features = pd.DataFrame(index=bars.index)
            features["sma_5"] = bars["close"].rolling(window=5).mean()
            features["sma_10"] = bars["close"].rolling(window=10).mean()
            features["sma_20"] = bars["close"].rolling(window=20).mean()
            features["sma_50"] = bars["close"].rolling(window=50).mean()
            features.dropna(inplace=True)
            return features
        except Exception as e:
            logging.error(f"Error creating features with pandas-ta: {e}")
            return pd.DataFrame()  # Return empty dataframe on error

    def _prepare_labels(
        self, bars: pd.DataFrame, look_forward=5, risk_reward_ratio=2.0
    ) -> pd.Series:
        """
        Creates labels for training based on a risk/reward outcome.
        - 1 (Buy): If the price hits the take profit target before the stop loss target.
        - 0 (Sell/Hold): If the price hits the stop loss target first or does nothing.
        """
        atr = self._calculate_atr(bars)
        labels = pd.Series(0, index=bars.index)

        for i in range(len(bars) - look_forward):
            entry_price = bars["close"].iloc[i]
            atr_value = atr.iloc[i]

            if pd.isna(atr_value) or atr_value == 0:
                continue

            stop_loss_price = entry_price - atr_value
            take_profit_price = entry_price + (atr_value * risk_reward_ratio)

            future_prices = bars["close"].iloc[i + 1 : i + 1 + look_forward]

            hit_tp = (future_prices >= take_profit_price).any()
            hit_sl = (future_prices <= stop_loss_price).any()

            if hit_tp and not hit_sl:
                labels.iloc[i] = 1  # Buy signal
            # The default is 0, so we don't need an explicit else for sell/hold

        return labels

    def train(self, symbol, timeframe="1Day", start_date=None, end_date=None):
        logging.info(f"Starting Advanced AI model training for {symbol}...")
        try:
            self.message_queue.put(
                {"type": "training_status", "data": {"status": "Fetching historical data..."}}
            )
            logging.info("Fetching bars...")
            bars = self.alpaca_service.get_bars(
                symbol, timeframe, start=start_date, end=end_date
            ).df
            logging.info(f"Fetched {len(bars)} bars.")
            if len(bars) < 100:
                logging.error("Not enough historical data to train the model.")
                self.message_queue.put(
                    {"type": "training_status", "data": {"status": "Error: Not enough data.", "error": True}}
                )
                return {"error": "Not enough data."}

            self.message_queue.put(
                {"type": "training_status", "data": {"status": "Preparing features..."}}
            )
            logging.info("Preparing features...")
            features = self._prepare_features(bars)
            self.message_queue.put(
                {"type": "training_status", "data": {"status": "Preparing labels..."}}
            )
            logging.info("Preparing labels...")
            labels = self._prepare_labels(bars)

            common_index = features.index.intersection(labels.index)
            features = features.loc[common_index]
            labels = labels.loc[common_index]

            if len(features) == 0:
                logging.error("Feature preparation resulted in empty data.")
                self.message_queue.put(
                    {"type": "training_status", "data": {"status": "Error: Could not prepare features.", "error": True}}
                )
                return {"error": "Could not prepare features."}

            self.message_queue.put(
                {"type": "training_status", "data": {"status": "Splitting data..."}}
            )
            logging.info("Splitting data...")
            X_train, X_test, y_train, y_test = train_test_split(
                features, labels, test_size=0.2, random_state=42, stratify=labels
            )

            self.message_queue.put(
                {"type": "training_status", "data": {"status": "Training model..."}}
            )
            logging.info("Training model...")
            self.model = xgb.XGBClassifier(
                objective="binary:logistic",
                eval_metric="logloss",
                use_label_encoder=False,
                n_estimators=200,
                learning_rate=0.05,
                max_depth=5,
                subsample=0.8,
                colsample_bytree=0.8,
            )
            self.model.fit(X_train, y_train)

            self.message_queue.put(
                {"type": "training_status", "data": {"status": "Calculating accuracy..."}}
            )
            logging.info("Calculating accuracy...")
            accuracy = self.model.score(X_test, y_test)
            logging.info(f"Model training complete. Accuracy: {accuracy:.2f}")
            self._save_model()
            self.message_queue.put(
                {"type": "training_status", "data": {"status": "Training complete!", "accuracy": accuracy, "error": False}}
            )
            return {"message": "Training successful", "accuracy": accuracy}

        except Exception as e:
            logging.error(f"An error occurred during training: {e}")
            logging.error(traceback.format_exc())
            self.message_queue.put(
                {"type": "training_status", "data": {"status": f"Error: {e}", "error": True}}
            )
            return {"error": str(e)}

    def generate_signals(self, bars: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=bars.index)
        signals["signal"] = 0
        signals["position"] = 0

        if not self.model:
            logging.warning("AI model is not trained. Cannot generate signals.")
            return signals

        features = self._prepare_features(bars)
        if not features.empty:
            predictions = self.model.predict(features)
            signals.loc[features.index, "signal"] = predictions
            signals["position"] = signals["signal"].diff()

        return signals

    async def run(self, symbol, timeframe, db_session):
        logging.info(f"Running AI Strategy for {symbol}")

        if not self.model:
            logging.warning("AI model is not trained. Cannot run live strategy.")
            return

        # Fetch latest data to make a prediction
        bars_data = self.alpaca_service.get_bars(
            symbol, timeframe, limit=100
        )  # Need enough for feature calculation
        if not bars_data or bars_data.df.empty:
            logging.warning(f"Could not fetch bars for {symbol} for AI prediction.")
            return

        bars = bars_data.df
        features = self._prepare_features(bars)

        if features.empty:
            logging.warning("Could not generate features for live prediction.")
            return

        # Predict the next move
        prediction = self.model.predict(features.tail(1))[0]
        current_position_qty = await self.get_position(symbol)

        if prediction == 1 and current_position_qty == 0:  # Buy signal
            last_price = bars["close"].iloc[-1]
            atr = self.risk_manager.calculate_atr(bars).iloc[-1]
            stop_loss_price = self.risk_manager.calculate_stop_loss(last_price, atr)
            qty_to_buy = self.risk_manager.calculate_position_size(
                last_price, stop_loss_price
            )

            if qty_to_buy > 0:
                take_profit_price = last_price + (last_price - stop_loss_price) * 2
                message = f"AI TRADE SIGNAL: Buy {symbol} at {last_price:.2f}"
                logging.info(message)
                await self.telegram_service.send_message(message)
                self.alpaca_service.submit_order(
                    symbol=symbol,
                    qty=qty_to_buy,
                    side="buy",
                    type="market",
                    time_in_force="day",
                    order_class="bracket",
                    take_profit={"limit_price": round(take_profit_price, 2)},
                    stop_loss={"stop_price": round(stop_loss_price, 2)},
                )
        elif prediction == 0 and current_position_qty > 0:
            logging.info(f"AI TRADE SIGNAL: Sell {symbol}. Closing position.")
            self.alpaca_service.api.close_position(symbol)
        else:
            logging.info(f"AI Strategy: No signal or position aligned for {symbol}.")

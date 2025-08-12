import logging
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from app.strategies.base import BaseStrategy

MODEL_PATH = "./trained_models/ai_strategy_model.joblib"

class AIStrategy(BaseStrategy):
    def __init__(self, alpaca_service, risk_manager, name="AI Strategy"):
        super().__init__(alpaca_service, risk_manager, name)
        self.model = self._load_model()

    def _load_model(self):
        try:
            model = joblib.load(MODEL_PATH)
            logging.info("AI model loaded successfully from disk.")
            return model
        except FileNotFoundError:
            logging.warning("No pre-trained model found. The model needs to be trained.")
            return None

    def _save_model(self):
        if self.model:
            joblib.dump(self.model, MODEL_PATH)
            logging.info(f"AI model saved to {MODEL_PATH}")

    def _prepare_features(self, bars: pd.DataFrame) -> pd.DataFrame:
        """Creates features for the model."""
        features = pd.DataFrame(index=bars.index)
        # Add features like RSI, MACD, Bollinger Bands, etc.
        # For simplicity, we'll start with a few moving average crossovers.
        features['sma_5'] = bars['close'].rolling(window=5).mean()
        features['sma_10'] = bars['close'].rolling(window=10).mean()
        features['sma_20'] = bars['close'].rolling(window=20).mean()
        features['sma_50'] = bars['close'].rolling(window=50).mean()
        features.dropna(inplace=True)
        return features

    def _prepare_labels(self, bars: pd.DataFrame) -> pd.Series:
        """Creates labels for training. Predict if the price will be higher or lower in the future."""
        labels = pd.Series(index=bars.index, dtype=int, name="target")
        # 1 if price is higher 5 bars from now, 0 otherwise
        labels = np.where(bars['close'].shift(-5) > bars['close'], 1, 0)
        return pd.Series(labels, index=bars.index)

    def train(self, symbol, timeframe='1Day', start_date=None, end_date=None):
        logging.info(f"Starting AI model training for {symbol}...")
        try:
            bars = self.alpaca_service.get_bars(symbol, timeframe, start=start_date, end=end_date).df
            if len(bars) < 100: # Need enough data to train
                logging.error("Not enough historical data to train the model.")
                return {"error": "Not enough data."}

            features = self._prepare_features(bars)
            labels = self._prepare_labels(bars)

            # Align data
            common_index = features.index.intersection(labels.index)
            features = features.loc[common_index]
            labels = labels.loc[common_index]

            if len(features) == 0:
                logging.error("Feature preparation resulted in empty data.")
                return {"error": "Could not prepare features."}

            X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

            self.model = LogisticRegression(max_iter=1000)
            self.model.fit(X_train, y_train)

            accuracy = self.model.score(X_test, y_test)
            logging.info(f"Model training complete. Accuracy: {accuracy:.2f}")
            self._save_model()
            return {"message": "Training successful", "accuracy": accuracy}

        except Exception as e:
            logging.error(f"An error occurred during training: {e}")
            return {"error": str(e)}

    def generate_signals(self, bars: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=bars.index)
        signals['signal'] = 0
        signals['position'] = 0

        if not self.model:
            logging.warning("AI model is not trained. Cannot generate signals.")
            return signals

        features = self._prepare_features(bars)
        if not features.empty:
            predictions = self.model.predict(features)
            signals.loc[features.index, 'signal'] = predictions
            signals['position'] = signals['signal'].diff()
        
        return signals

    async def run(self, symbol, timeframe, db_session):
        logging.info(f"Running AI Strategy for {symbol}")

        if not self.model:
            logging.warning("AI model is not trained. Cannot run live strategy.")
            return

        # Fetch latest data to make a prediction
        bars_data = self.alpaca_service.get_bars(symbol, timeframe, limit=100) # Need enough for feature calculation
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

        if prediction == 1 and current_position_qty == 0: # Buy signal
            last_price = bars['close'].iloc[-1]
            atr = self.risk_manager.calculate_atr(bars).iloc[-1]
            stop_loss_price = self.risk_manager.calculate_stop_loss(last_price, atr)
            qty_to_buy = self.risk_manager.calculate_position_size(last_price, stop_loss_price)

            if qty_to_buy > 0:
                take_profit_price = last_price + (last_price - stop_loss_price) * 2
                message = f"AI TRADE SIGNAL: Buy {symbol} at {last_price:.2f}"
                logging.info(message)
                await self.telegram_service.send_message(message)
                self.alpaca_service.submit_order(
                    symbol=symbol, qty=qty_to_buy, side='buy', type='market', time_in_force='day',
                    order_class='bracket', take_profit={'limit_price': round(take_profit_price, 2)},
                    stop_loss={'stop_price': round(stop_loss_price, 2)}
                )
        elif prediction == 0 and current_position_qty > 0: # Sell signal
            logging.info(f"AI TRADE SIGNAL: Sell {symbol}. Closing position.")
            self.alpaca_service.api.close_position(symbol)
        else:
            logging.info(f"AI Strategy: No signal or position aligned for {symbol}.")

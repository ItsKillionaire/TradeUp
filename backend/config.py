from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    ALPACA_API_KEY: str = Field(..., description="Alpaca API Key")
    ALPACA_SECRET_KEY: str = Field(..., description="Alpaca Secret Key")
    ALPACA_BASE_URL: str = Field("https://paper-api.alpaca.markets", description="Alpaca Base URL")
    TELEGRAM_BOT_TOKEN: str | None = Field(None, description="Telegram Bot Token")
    TELEGRAM_CHAT_ID: str | None = Field(None, description="Telegram Chat ID")
    SECRET_KEY: str = Field("your-super-secret-key", description="Secret key for JWT. CHANGE THIS IN PRODUCTION!")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, description="Access token expiration time in minutes")

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "dev"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "postgresql+psycopg://stock:stock@localhost:5432/stock"
    redis_url: str = "redis://localhost:6379/0"
    
    news_provider: str = "marketaux"
    news_api_key: str | None = None
    news_poll_seconds: int = 60
    news_window_minutes: int = 60
    
    alpaca_api_key: str | None = None
    alpaca_api_secret: str | None = None
    alpaca_base_url: str = "https://paper-api.alpaca.markets"
    alpaca_id: str = "921556744"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
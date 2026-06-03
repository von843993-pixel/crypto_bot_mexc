"""
═══════════════════════════════════
Load Configuration từ .env
═══════════════════════════════════
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from .schema import AppConfig, MexcConfig, TradingConfig, DatabaseConfig, RabbitMQConfig, TelegramConfig, OllamaConfig

def load_config() -> AppConfig:
    """
    Tải config từ .env file
    """
    # Load .env
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    
    # Build config từ environment variables
    config = AppConfig(
        mexc=MexcConfig(
            api_key=os.getenv("MEXC_API_KEY", ""),
            api_secret=os.getenv("MEXC_API_SECRET", ""),
            testnet=os.getenv("MEXC_TESTNET", "false").lower() == "true",
        ),
        trading=TradingConfig(
            mode=os.getenv("TRADING_MODE", "paper"),
            pairs=os.getenv("TRADING_PAIRS", "BTC/USDT,ETH/USDT").split(","),
            initial_capital=float(os.getenv("INITIAL_CAPITAL", "200")),
            position_size_percent=float(os.getenv("POSITION_SIZE_PERCENT", "0.5")),
            stop_loss_percent=float(os.getenv("STOP_LOSS_PERCENT", "1.5")),
            take_profit_percent=float(os.getenv("TAKE_PROFIT_PERCENT", "0.8")),
            max_daily_loss_percent=float(os.getenv("MAX_DAILY_LOSS_PERCENT", "5.0")),
        ),
        database=DatabaseConfig(
            mode=os.getenv("DB_MODE", "sqlite"),
            sqlite_path=Path(os.getenv("DB_SQLITE_PATH", "data/trading.db")),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "trading_bot"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
        ),
        rabbitmq=RabbitMQConfig(
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            port=int(os.getenv("RABBITMQ_PORT", "5672")),
            user=os.getenv("RABBITMQ_USER", "guest"),
            password=os.getenv("RABBITMQ_PASSWORD", "guest"),
            vhost=os.getenv("RABBITMQ_VHOST", "/"),
        ),
        telegram=TelegramConfig(
            enabled=os.getenv("TELEGRAM_ENABLED", "true").lower() == "true",
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        ),
        ollama=OllamaConfig(
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "phi3"),
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        prometheus_port=int(os.getenv("PROMETHEUS_PORT", "8000")),
    )
    
    return config

# Global config instance
CONFIG = load_config()

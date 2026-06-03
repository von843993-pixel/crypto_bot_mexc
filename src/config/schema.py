"""
═══════════════════════════════════
Config Schema - Định nghĩa cấu hình
═══════════════════════════════════
"""
from pydantic import BaseModel, Field
from typing import Literal, List
from pathlib import Path

class MexcConfig(BaseModel):
    """Cấu hình MEXC API"""
    api_key: str
    api_secret: str
    testnet: bool = False
    timeout: int = 10

class TradingConfig(BaseModel):
    """Cấu hình trading parameters"""
    mode: Literal["paper", "live"] = "paper"
    pairs: List[str] = Field(default=["BTC/USDT", "ETH/USDT"])
    initial_capital: float = 200.0
    position_size_percent: float = 0.5
    
    # Risk Management
    stop_loss_percent: float = 1.5
    take_profit_percent: float = 0.8
    max_daily_loss_percent: float = 5.0
    
    # Timeframes
    timeframes: List[str] = Field(default=["1m", "5m", "15m"])

class DatabaseConfig(BaseModel):
    """Cấu hình Database"""
    mode: Literal["sqlite", "timescaledb"] = "sqlite"
    sqlite_path: Path = Path("data/trading.db")
    
    # TimescaleDB
    host: str = "localhost"
    port: int = 5432
    name: str = "trading_bot"
    user: str = "postgres"
    password: str = "postgres"

class RabbitMQConfig(BaseModel):
    """Cấu hình RabbitMQ"""
    host: str = "localhost"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"
    vhost: str = "/"

class TelegramConfig(BaseModel):
    """Cấu hình Telegram"""
    enabled: bool = True
    bot_token: str
    chat_id: str

class OllamaConfig(BaseModel):
    """Cấu hình Ollama LLM"""
    host: str = "http://localhost:11434"
    model: str = "phi3"
    timeout: int = 30

class AppConfig(BaseModel):
    """Cấu hình chính của ứng dụng"""
    mexc: MexcConfig
    trading: TradingConfig
    database: DatabaseConfig
    rabbitmq: RabbitMQConfig
    telegram: TelegramConfig
    ollama: OllamaConfig
    
    # Logging
    log_level: str = "INFO"
    log_dir: Path = Path("logs")
    
    # Monitoring
    prometheus_port: int = 8000
    health_check_interval: int = 30
    watchdog_interval: int = 60
    
    class Config:
        env_nested_delimiter = "__"

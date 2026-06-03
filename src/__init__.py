"""
═══════════════════════════════════════════════════════════════
CRYPTO BOT MEXC - Enterprise AI Trading Bot
═══════════════════════════════════════════════════════════════

Lightweight trading bot cho MEXC:
- CPU only (không cần GPU)
- Async + Event-driven
- Q-Learning + XGBoost + LightGBM + Ollama LLM
- Paper → Live auto-promotion
- Full risk management + compound

Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Trading Team"

from src.config.base import CONFIG

__all__ = ["CONFIG"]

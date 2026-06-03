"""
═══════════════════════════════════════════════════════════════
Bollinger Bands - Volatility indicator
═══════════════════════════════════════════════════════════════
"""
import numpy as np
from typing import Dict, Any, Optional

class BollingerBands:
    """Bollinger Bands indicator"""
    
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        """Initialize Bollinger Bands"""
        self.period = period
        self.std_dev = std_dev
    
    def calculate(self, close: np.ndarray) -> Optional[Dict[str, Any]]:
        """Calculate Bollinger Bands"""
        if len(close) < self.period:
            return None
        
        # Calculate SMA and standard deviation
        sma = np.mean(close[-self.period:])
        std = np.std(close[-self.period:])
        
        # Calculate bands
        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)
        
        current_price = close[-1]
        
        # Calculate bandwidth
        bandwidth = (upper_band - lower_band) / sma * 100
        
        # Signal generation
        signal = "NEUTRAL"
        if current_price < lower_band:
            signal = "OVERSOLD"
        elif current_price > upper_band:
            signal = "OVERBOUGHT"
        elif current_price > sma:
            signal = "BULLISH"
        elif current_price < sma:
            signal = "BEARISH"
        
        # Calculate %B (position within bands)
        percent_b = (current_price - lower_band) / (upper_band - lower_band) * 100
        
        return {
            "upper_band": upper_band,
            "middle_band": sma,
            "lower_band": lower_band,
            "bandwidth": bandwidth,
            "percent_b": percent_b,
            "signal": signal,
            "squeeze": bandwidth < 5,  # Squeeze when bands are tight
        }

"""
═══════════════════════════════════════════════════════════════
RSI Adaptive - Self-adjusting RSI indicator
═══════════════════════════════════════════════════════════════
"""
import numpy as np
from typing import Dict, Any, Optional

class RSIAdaptive:
    """RSI with adaptive thresholds"""
    
    def __init__(self, period: int = 14):
        """Initialize RSI Adaptive"""
        self.period = period
    
    def calculate(self, close: np.ndarray) -> Optional[Dict[str, Any]]:
        """Calculate RSI with adaptive thresholds"""
        if len(close) < self.period:
            return None
        
        try:
            import talib
            rsi = talib.RSI(close, timeperiod=self.period)[-1]
        except ImportError:
            # Fallback calculation
            rsi = self._calculate_rsi_manual(close[-self.period:])
        
        # Calculate volatility
        returns = np.diff(close) / close[:-1]
        volatility = np.std(returns[-20:]) if len(returns) >= 20 else 0
        
        # Calculate momentum
        momentum = close[-1] - close[-20] if len(close) >= 20 else 0
        momentum_pct = (momentum / close[-21]) * 100 if len(close) > 20 and close[-21] != 0 else 0
        
        # Determine market regime
        if abs(momentum_pct) > 2 and volatility > 0.02:
            oversold = 40
            overbought = 60
            regime = "trending"
        elif volatility < 0.01:
            oversold = 30
            overbought = 70
            regime = "sideways"
        else:
            oversold = 25
            overbought = 75
            regime = "volatile"
        
        # Signal
        signal = "NEUTRAL"
        if rsi < oversold:
            signal = "OVERSOLD"
        elif rsi > overbought:
            signal = "OVERBOUGHT"
        
        return {
            "rsi": rsi,
            "oversold": oversold,
            "overbought": overbought,
            "signal": signal,
            "regime": regime,
            "volatility": volatility,
            "momentum_pct": momentum_pct,
        }
    
    def _calculate_rsi_manual(self, prices: np.ndarray) -> float:
        """Manual RSI calculation"""
        deltas = np.diff(prices)
        seed = deltas[:1]
        up = seed * np.nan
        down = -seed * np.nan
        
        for i in range(1, len(deltas)):
            if deltas[i] >= 0:
                up = np.append(up, deltas[i])
                down = np.append(down, 0)
            else:
                up = np.append(up, 0)
                down = np.append(down, -deltas[i])
        
        up_avg = np.nanmean(up)
        down_avg = np.nanmean(down)
        
        if down_avg == 0:
            return 100
        
        rs = up_avg / down_avg
        rsi = 100 - (100 / (1 + rs))
        
        return rsi

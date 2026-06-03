"""
═══════════════════════════════════════════════════════════════
OBV - On Balance Volume indicator
═══════════════════════════════════════════════════════════════
"""
import numpy as np
from typing import Dict, Any, Optional

class OBV:
    """On Balance Volume indicator"""
    
    def __init__(self):
        """Initialize OBV"""
        self.obv = None
    
    def calculate(
        self,
        close: np.ndarray,
        volume: np.ndarray,
    ) -> Optional[Dict[str, Any]]:
        """Calculate OBV"""
        if len(close) < 2:
            return None
        
        obv = np.zeros(len(close))
        obv[0] = volume[0]
        
        for i in range(1, len(close)):
            if close[i] > close[i-1]:
                obv[i] = obv[i-1] + volume[i]
            elif close[i] < close[i-1]:
                obv[i] = obv[i-1] - volume[i]
            else:
                obv[i] = obv[i-1]
        
        # Calculate OBV signal (EMA of OBV)
        obv_series = obv[-20:]
        obv_ema = np.mean(obv_series)
        
        # Determine signal
        current_obv = obv[-1]
        signal = "NEUTRAL"
        
        if current_obv > obv_ema:
            signal = "BULLISH"
        elif current_obv < obv_ema:
            signal = "BEARISH"
        
        return {
            "obv": current_obv,
            "obv_ema": obv_ema,
            "signal": signal,
            "momentum": current_obv - obv[-2] if len(obv) > 1 else 0,
        }

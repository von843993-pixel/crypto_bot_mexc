"""
═══════════════════════════════════════════════════════════════
Hybrid Trading Flow - Main trading loop
═══════════════════════════════════════════════════════════════
"""
import asyncio
from datetime import datetime, date
from typing import Optional
from ...core.logger import trade_logger
from ...core.types import TradeDirection
from ...config.schema import AppConfig
from ...data.sources.mexc import MexcClient
from ...data.storage.sqlite import SQLiteDB
from ...notifications.telegram import TelegramBot

class HybridFlow:
    """Main trading orchestrator"""
    
    def __init__(
        self,
        mexc_client: MexcClient,
        db: SQLiteDB,
        telegram_bot: Optional[TelegramBot],
        config: AppConfig,
    ):
        """Initialize trading flow"""
        self.mexc = mexc_client
        self.db = db
        self.telegram = telegram_bot
        self.config = config
        
        self.is_running = False
        self.balance = config.trading.initial_capital
        self.positions = {}
        self.daily_trades = 0
        self.daily_pnl = 0.0
    
    async def step(self):
        """One trading step (runs every 1 minute)"""
        try:
            # 1. Fetch data
            for symbol in self.config.trading.pairs:
                await self._fetch_and_update(symbol)
            
            # 2. Calculate indicators
            for symbol in self.config.trading.pairs:
                await self._calculate_indicators(symbol)
            
            # 3. Fusion signals
            for symbol in self.config.trading.pairs:
                await self._fusion_signals(symbol)
            
            # 4. Execute trades
            await self._execute_trades()
            
        except Exception as e:
            trade_logger.error(f"Step error: {e}")
    
    async def _fetch_and_update(self, symbol: str):
        """Fetch latest data from MEXC"""
        try:
            ohlcv = await self.mexc.fetch_ohlcv(symbol, "1m", limit=1)
            
            if ohlcv:
                from ...core.types import OHLCV
                candle = ohlcv[0]
                ohlcv_obj = OHLCV(
                    timestamp=datetime.fromtimestamp(candle[0] / 1000),
                    open=candle[1],
                    high=candle[2],
                    low=candle[3],
                    close=candle[4],
                    volume=candle[5],
                    symbol=symbol,
                    timeframe="1m",
                )
                
                await self.db.insert_ohlcv(ohlcv_obj)
                
        except Exception as e:
            trade_logger.error(f"Fetch error ({symbol}): {e}")
    
    async def _calculate_indicators(self, symbol: str):
        """Calculate all indicators"""
        try:
            ohlcv_data = await self.db.fetch_ohlcv(symbol, "1m", limit=100)
            
            if len(ohlcv_data) < 50:
                return
            
            import numpy as np
            closes = np.array([x.close for x in ohlcv_data])
            
            # TODO: Add indicator calculations
            
        except Exception as e:
            trade_logger.error(f"Indicator error ({symbol}): {e}")
    
    async def _fusion_signals(self, symbol: str):
        """Fuse signals from multiple sources"""
        # TODO: Implement signal fusion
        pass
    
    async def _execute_trades(self):
        """Execute trades"""
        # TODO: Implement execution
        pass
    
    async def optimize_models(self):
        """Optimize models (every 6 hours)"""
        trade_logger.info("Optimizing models...")
        # TODO: Implement model optimization
    
    async def daily_summary(self):
        """Daily summary (23:59)"""
        today = date.today()
        from datetime import datetime as dt
        trades = await self.db.get_trades_by_date(dt.combine(today, dt.min.time()))
        
        if not trades:
            return
        
        winning_trades = sum(1 for t in trades if t.is_profitable)
        losing_trades = len(trades) - winning_trades
        win_rate = winning_trades / len(trades) * 100 if trades else 0
        total_pnl = sum(t.pnl or 0 for t in trades)
        
        summary = f"""
📊 **DAILY SUMMARY - {today}**

📈 Trades: {len(trades)}
✅ Win: {winning_trades} | ❌ Loss: {losing_trades}
🏆 Win Rate: {win_rate:.1f}%
💰 Total P&L: ${total_pnl:.2f}
"""
        
        if self.telegram:
            await self.telegram.send_message(summary)
        
        trade_logger.info(summary)
    
    async def stop(self):
        """Stop bot"""
        self.is_running = False

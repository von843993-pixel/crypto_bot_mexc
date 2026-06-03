"""
═══════════════════════════════════════════════════════════════
MEXC Exchange Client - Connect to MEXC
═══════════════════════════════════════════════════════════════
"""
import asyncio
import ccxt
import ccxt.async_support as ccxt_async
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..core.logger import exchange_logger
from ..core.exceptions import ExchangeException, DataFetchException
from ..core.types import OHLCV

class MexcClient:
    """MEXC exchange client"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        """Initialize MEXC client"""
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        self.exchange = ccxt.mexc({
            'apiKey': api_key,
            'secret': api_secret,
            'sandbox': testnet,
            'enableRateLimit': True,
        })
        
        self.exchange_async = None
        exchange_logger.info(f"MEXC client initialized (testnet={testnet})")
    
    async def init_async(self):
        """Initialize async client"""
        self.exchange_async = ccxt_async.mexc({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'sandbox': self.testnet,
            'enableRateLimit': True,
        })
    
    async def close_async(self):
        """Close async client"""
        if self.exchange_async:
            await self.exchange_async.close()
    
    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
    ) -> List[List]:
        """Fetch OHLCV candlesticks"""
        try:
            if not self.exchange_async:
                await self.init_async()
            
            ohlcv = await self.exchange_async.fetch_ohlcv(
                symbol,
                timeframe,
                limit=limit,
            )
            
            exchange_logger.debug(f"Fetched {len(ohlcv)} candles")
            return ohlcv
            
        except Exception as e:
            exchange_logger.error(f"OHLCV fetch failed: {e}")
            raise DataFetchException(f"Cannot fetch OHLCV: {e}")
    
    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """Fetch ticker"""
        try:
            if not self.exchange_async:
                await self.init_async()
            
            ticker = await self.exchange_async.fetch_ticker(symbol)
            return ticker
            
        except Exception as e:
            exchange_logger.error(f"Ticker fetch failed: {e}")
            raise DataFetchException(f"Cannot fetch ticker: {e}")
    
    async def fetch_balance(self) -> Dict[str, Any]:
        """Fetch balance"""
        try:
            if not self.exchange_async:
                await self.init_async()
            
            balance = await self.exchange_async.fetch_balance()
            return balance
            
        except Exception as e:
            exchange_logger.error(f"Balance fetch failed: {e}")
            raise ExchangeException(f"Cannot fetch balance: {e}")
    
    async def place_order(
        self,
        symbol: str,
        order_type: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Place order"""
        try:
            if not self.exchange_async:
                await self.init_async()
            
            order = await self.exchange_async.create_order(
                symbol,
                order_type,
                side,
                amount,
                price,
            )
            
            exchange_logger.info(f"Order placed: {order.get('id')}")
            return order
            
        except Exception as e:
            exchange_logger.error(f"Order placement failed: {e}")
            raise ExchangeException(f"Cannot place order: {e}")
    
    async def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel order"""
        try:
            if not self.exchange_async:
                await self.init_async()
            
            result = await self.exchange_async.cancel_order(order_id, symbol)
            exchange_logger.info(f"Order cancelled: {order_id}")
            return result
            
        except Exception as e:
            exchange_logger.error(f"Cancel order failed: {e}")
            raise ExchangeException(f"Cannot cancel order: {e}")

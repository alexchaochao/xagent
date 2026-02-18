import ccxt
import pandas as pd
import numpy as np
from typing import Optional
import time

def fetch_ohlcv(symbol: str = "BTCUSDT", timeframe: str = "4h", limit: int = 200, exchange: Optional[ccxt.Exchange]=None) -> pd.DataFrame:
    """Fetch OHLCV from Binance via CCXT and return a pandas DataFrame with columns: ts, open, high, low, close, volume.

    If network fails, return a synthetic sample DataFrame so the pipeline can run offline.
    """
    if exchange is None:
        exchange = ccxt.binance({"enableRateLimit": True})

    # normalize symbol to ccxt format if necessary
    if "/" not in symbol:
        # common mapping: BTCUSDT -> BTC/USDT
        if symbol.endswith("USDT"):
            symbol = symbol[:-4] + "/USDT"
        elif symbol.endswith("USD"):
            symbol = symbol[:-3] + "/USD"

    try:
        # ccxt uses symbol format like 'BTC/USDT'
        data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(data, columns=["ts", "open", "high", "low", "close", "volume"]) 
        df["ts"] = pd.to_datetime(df["ts"], unit="ms")
        df.set_index("ts", inplace=True)
        return df
    except Exception as e:
        # fallback: synthetic random-walk candles
        now = int(time.time())
        periods = limit
        # create hourly timestamps
        idx = pd.date_range(end=pd.to_datetime(now, unit="s"), periods=periods, freq='H')
        price = 30000.0
        closes = price * np.cumprod(1 + np.random.normal(0, 0.001, size=periods))
        opens = np.concatenate([[price], closes[:-1]])
        highs = np.maximum(opens, closes) * (1 + np.abs(np.random.normal(0, 0.002, size=periods)))
        lows = np.minimum(opens, closes) * (1 - np.abs(np.random.normal(0, 0.002, size=periods)))
        volume = np.random.uniform(10, 1000, size=periods)
        df = pd.DataFrame({"open": opens, "high": highs, "low": lows, "close": closes, "volume": volume}, index=idx)
        df.index.name = "ts"
        return df

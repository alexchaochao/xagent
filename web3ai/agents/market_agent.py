import pandas as pd
import numpy as np
from typing import Dict
import math

def analyze_market(klines: pd.DataFrame) -> Dict:
    """Enhanced MarketAgent producing `technical_evidence` as requested.

    Computes trend, risk_level, reason and technical evidence fields:
    - price_break_structure: boolean
    - ma_cross: 'bullish'|'bearish'|'neutral'
    - open_interest_change_pct: simulated (placeholder)
    - funding_rate: simulated (placeholder)
    """
    df = klines.copy()
    df["ma50"] = df["close"].rolling(50, min_periods=1).mean()
    df["ma200"] = df["close"].rolling(200, min_periods=1).mean()
    df["returns"] = df["close"].pct_change().fillna(0)
    vol = df["returns"].rolling(50).std().iloc[-1]

    price = float(df["close"].iloc[-1])
    ma50 = float(df["ma50"].iloc[-1])
    ma200 = float(df["ma200"].iloc[-1])

    # trend and ma_cross
    if ma50 > ma200:
        trend = "bullish"
        ma_cross = "bullish"
        reason = "MA50 above MA200"
    elif ma50 < ma200:
        trend = "bearish"
        ma_cross = "bearish"
        reason = "MA50 below MA200"
    else:
        trend = "neutral"
        ma_cross = "neutral"
        reason = "moving averages mixed"

    # price_break_structure: check whether last close breaks above the recent 20-bar high
    lookback = min(20, len(df)-1)
    if lookback >= 3:
        recent_high = df["high"].iloc[-(lookback+1):-1].max()
        price_break_structure = price > recent_high
    else:
        price_break_structure = False

    # simulate open interest and funding rate for prototype (replace with real API later)
    # open_interest_change_pct: small random-like heuristic based on recent volume change
    try:
        vol_now = float(df["volume"].iloc[-1])
        vol_prev = float(df["volume"].iloc[-2]) if len(df) > 2 else vol_now
        open_interest_change_pct = round(((vol_now - vol_prev) / max(1e-9, vol_prev)) * 100, 2)
    except Exception:
        open_interest_change_pct = 0.0

    # funding_rate: placeholder small value
    funding_rate = round(np.sign(price - df["close"].iloc[-2] if len(df) > 1 else 0) * 0.001, 5)

    # risk proxy
    if vol < 0.005:
        risk = "low"
    elif vol < 0.02:
        risk = "medium"
    else:
        risk = "high"

    technical_evidence = {
        "price_break_structure": bool(price_break_structure),
        "ma_cross": ma_cross,
        "open_interest_change_pct": float(open_interest_change_pct),
        "funding_rate": float(funding_rate),
    }

    return {
        "trend": trend,
        "risk_level": risk,
        "reason": reason,
        "volatility": float(vol),
        "technical_evidence": technical_evidence,
    }

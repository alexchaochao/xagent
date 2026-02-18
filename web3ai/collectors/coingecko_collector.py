import requests
from typing import Optional

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

def map_symbol_to_coingecko_id(symbol: str) -> str:
    s = symbol.upper()
    if s.startswith("BTC"):
        return "bitcoin"
    if s.startswith("ETH"):
        return "ethereum"
    # default fallback
    return s.lower()


def get_exchange_netflow_btc(symbol: str, api_key: Optional[str] = None) -> Optional[int]:
    """Best-effort proxy for exchange netflow using Coingecko market volume change.

    Coingecko does not provide direct exchange netflow; we approximate by comparing
    recent total traded volume over two windows (e.g., last 24h vs previous 24h) and
    return a signed integer as a proxy (positive -> inflow, negative -> outflow).
    """
    try:
        coin_id = map_symbol_to_coingecko_id(symbol)
        # fetch 2 days of market chart data (hourly) to compute 24h totals
        url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd", "days": "2", "interval": "hourly"}
        headers = {}
        if api_key:
            # Accept custom API key header if provided (some proxies may require it)
            headers["x-api-key"] = api_key
        r = requests.get(url, params=params, headers=headers or None, timeout=15)
        r.raise_for_status()
        data = r.json()
        volumes = data.get("total_volumes") or []
        if len(volumes) < 24:
            return None

        # volumes: list of [ts, volume]; compute sum last 24 hours vs previous 24 hours
        # take last 48 points if available
        last_n = 24
        vals = [v[1] for v in volumes]
        if len(vals) < last_n * 2:
            # fallback: use available slice
            last_sum = sum(vals[-last_n:])
            prev_sum = sum(vals[:-last_n]) if len(vals) > last_n else 0
        else:
            last_sum = sum(vals[-last_n:])
            prev_sum = sum(vals[-last_n*2:-last_n])

        # difference as proxy (signed), scale down to BTC units by assuming price ~1? we'll return integer proxy
        diff = last_sum - prev_sum
        # convert to int (could be large), we scale to millions to keep numbers manageable
        proxy = int(diff / 1e6)
        return proxy
    except Exception:
        return None

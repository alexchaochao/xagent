import requests
from typing import Optional

COINGLASS_BASE = "https://open-api.coinglass.com"

def get_exchange_netflow_btc(symbol: str, api_key: str) -> Optional[int]:
    """Attempt to fetch exchange netflow for symbol from Coinglass.

    This is a best-effort prototype call because Coinglass endpoints vary by plan.
    Returns integer netflow in BTC if available, otherwise None.
    """
    try:
        # Example endpoint (may require pro access). We use a generic path and API key header.
        url = f"{COINGLASS_BASE}/api/v2/flow/netflow"
        headers = {"coinglass-api-key": api_key}
        params = {"symbol": symbol}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        # attempt to extract a plausible field
        if isinstance(data, dict):
            # many Coinglass endpoints return {code:0, data: {...}}
            payload = data.get("data") or data
            netflow = payload.get("netFlow") or payload.get("netflow") or payload.get("net_flow")
            if netflow is not None:
                return int(float(netflow))
    except Exception:
        return None

    return None

import requests
from typing import Optional, List, Dict

ETHERSCAN_BASE = "https://api.etherscan.io/api"

def get_token_supply(contract_address: str, api_key: str) -> Optional[int]:
    try:
        params = {
            "module": "stats",
            "action": "tokensupply",
            "contractaddress": contract_address,
            "apikey": api_key,
        }
        r = requests.get(ETHERSCAN_BASE, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "1":
            return int(data.get("result"))
    except Exception:
        return None

    return None


def get_recent_token_transfers(contract_address: str, api_key: str, page: int = 1, offset: int = 100) -> List[Dict]:
    """Fetch recent ERC20 token transfers for a contract (descending)."""
    try:
        params = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": contract_address,
            "page": page,
            "offset": offset,
            "sort": "desc",
            "apikey": api_key,
        }
        r = requests.get(ETHERSCAN_BASE, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "1":
            return data.get("result", [])
    except Exception:
        return []

    return []

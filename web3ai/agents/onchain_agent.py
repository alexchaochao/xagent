from typing import Dict
import random
import os

from web3ai.collectors.etherscan_collector import get_token_supply, get_recent_token_transfers
from web3ai.collectors.coinglass_collector import get_exchange_netflow_btc as get_netflow_coinglass
from web3ai.collectors.coingecko_collector import get_exchange_netflow_btc as get_netflow_coingecko
from web3ai import config

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
COINGLASS_API_KEY = config.COINGLASS_API_KEY
COINGECKO_ENABLED = config.COINGECKO_ENABLED
COINGECKO_API_KEY = config.COINGECKO_API_KEY


def analyze_onchain() -> Dict:
    """OnchainAgent: try real APIs (Etherscan/Coinglass) if keys present, else fallback to simulated data."""
    flow = None
    whale = None
    confidence = None
    exchange_netflow_btc = None
    whale_transfer_detected = False
    whale_tx_hash = None
    stablecoin_supply_change = None

    exchange_netflow_source = "simulated"
    # Simplified: use Coingecko exclusively (if enabled) as requested; keep Coinglass file but do not call it
    if COINGECKO_ENABLED:
        try:
            exchange_netflow_btc = get_netflow_coingecko("BTC", api_key=COINGECKO_API_KEY)
            if exchange_netflow_btc is not None:
                flow = "inflow" if exchange_netflow_btc > 0 else "outflow"
                exchange_netflow_source = "coingecko"
        except Exception:
            exchange_netflow_btc = None

    # Try Etherscan for large stablecoin transfers and supply
    if ETHERSCAN_API_KEY:
        try:
            # Example: USDT contract (Ethereum mainnet)
            usdt_contract = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
            transfers = get_recent_token_transfers(usdt_contract, ETHERSCAN_API_KEY, page=1, offset=50)
            # find large transfers > 100k USDT
            for tx in transfers:
                try:
                    value = int(tx.get("value", 0))
                    decimals = int(tx.get("tokenDecimal", 6))
                    human = value / (10 ** decimals)
                    if human >= 100000:
                        whale_transfer_detected = True
                        whale_tx_hash = tx.get("hash")
                        break
                except Exception:
                    continue

            supply = get_token_supply(usdt_contract, ETHERSCAN_API_KEY)
            if supply:
                # show supply in millions
                stablecoin_supply_change = f"{round(supply / 1e6)}M"
        except Exception:
            whale_transfer_detected = whale_transfer_detected

    # If APIs didn't set values, fallback to simulation
    if flow is None:
        flow = random.choice(["inflow", "outflow", "neutral"])
    if whale is None:
        whale = random.choice(["accumulating", "distributing", "neutral"])
    if confidence is None:
        confidence = round(random.uniform(0.5, 0.95), 2)
    if exchange_netflow_btc is None:
        exchange_netflow_btc = int(round(random.uniform(-5000, 5000)))
    if stablecoin_supply_change is None:
        stablecoin_supply_change = f"{int(random.uniform(-500, 1000))}M"

    result = {
        "capital_flow": flow,
        "whale_behavior": whale,
        "confidence": confidence,
        "exchange_netflow_btc": exchange_netflow_btc,
        "whale_transfer_detected": whale_transfer_detected,
        "whale_tx_hash": whale_tx_hash,
        "stablecoin_supply_change": stablecoin_supply_change,
        "exchange_netflow_source": exchange_netflow_source,
    }

    return result

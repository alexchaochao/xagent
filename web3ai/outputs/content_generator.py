from typing import Dict

def generate_tweet(decision: Dict, market: Dict, onchain: Dict, sentiment: Dict) -> str:
    lines = []
    lines.append(f"Action: {decision['action']} (conf {decision['confidence']})")
    lines.append(f"Market: {market['trend']} - {market['reason']}")
    lines.append(f"Onchain: {onchain['capital_flow']} / {onchain['whale_behavior']}")
    if decision.get('risk_warning'):
        lines.append(f"Risk: {decision['risk_warning']}")
    return "\n".join(lines)

def generate_youtube_script(decision: Dict, market: Dict, onchain: Dict, sentiment: Dict) -> str:
    s = []
    s.append("Market update:")
    s.append(f"Technicals: {market['reason']}, current trend: {market['trend']}")
    s.append(f"On-chain: capital flow {onchain['capital_flow']}, whale behavior {onchain['whale_behavior']}")
    if decision.get('risk_warning'):
        s.append(f"Risk note: {decision['risk_warning']}")
    s.append(f"Recommendation: {decision['action']} (confidence {decision['confidence']})")
    return "\n\n".join(s)

def generate_structured_report(symbol: str, timeframe: str, decision: Dict, market: Dict, onchain: Dict, sentiment: Dict, data_sources=None) -> Dict:
    if data_sources is None:
        data_sources = ["Binance API", "Etherscan", "Coinglass"]

    report = {
        "symbol": symbol.replace('/', '').upper(),
        "timeframe": timeframe,
        "decision": {
            "action": decision.get("action"),
            "confidence": decision.get("confidence"),
            "score": decision.get("score"),
        },
        "technical_evidence": market.get("technical_evidence", {}),
        "onchain_evidence": {
            "exchange_netflow_btc": onchain.get("exchange_netflow_btc"),
            "exchange_netflow_source": onchain.get("exchange_netflow_source"),
            "whale_transfer_detected": onchain.get("whale_transfer_detected"),
            "whale_tx_hash": onchain.get("whale_tx_hash"),
            "stablecoin_supply_change": onchain.get("stablecoin_supply_change"),
        },
        "sentiment_evidence": {
            "fear_greed_index": sentiment.get("fear_greed_index"),
            "long_short_ratio": sentiment.get("long_short_ratio"),
            "liquidations_24h": sentiment.get("liquidations_24h"),
        },
        "data_sources": data_sources,
    }

    return report

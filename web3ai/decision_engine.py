from typing import Dict

def decide(market: Dict, onchain: Dict, sentiment: Dict) -> Dict:
    """Decision Engine implementing simple rule-based alpha and returning a numeric score.

    Returns: action, confidence, risk_warning, score
    """
    # base numeric confidence from market trend
    if market["trend"] == "bullish":
        market_score = 85
    elif market["trend"] == "bearish":
        market_score = 15
    else:
        market_score = 50

    # onchain contribution: prefer inflow
    if onchain.get("capital_flow") == "inflow":
        onchain_score = int(onchain.get("confidence", 0.6) * 100)
    elif onchain.get("capital_flow") == "outflow":
        onchain_score = int((1 - onchain.get("confidence", 0.6)) * 100)
    else:
        onchain_score = 50

    # sentiment contribution: scale fear_greed_index (0-100) directly
    fear_greed = int(sentiment.get("fear_greed_index", 50))

    # combine into 0-100 score (weighted)
    score = int((0.5 * market_score) + (0.3 * onchain_score) + (0.2 * fear_greed))

    # rules to decide action
    if market["trend"] == "bullish" and onchain.get("capital_flow") == "inflow" and fear_greed < 80:
        action = "LONG"
    elif market["trend"] == "bullish" and onchain.get("capital_flow") == "outflow" and fear_greed >= 80:
        action = "WAIT/SELL_SIGNAL"
    elif market["trend"] == "bearish":
        action = "SHORT_OR_STAY_OUT"
    else:
        action = "HOLD"

    # normalize confidence as score/100 with clamp
    confidence = max(0.0, min(1.0, score / 100.0))

    risk_warning = None
    if market.get("risk_level") == "high" or fear_greed >= 80:
        risk_warning = "Sentiment hot or market volatility high; watch risk"

    return {"action": action, "confidence": round(confidence, 2), "risk_warning": risk_warning, "score": score}

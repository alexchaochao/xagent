from typing import Dict
import random


def analyze_sentiment() -> Dict:
    """Enhanced SentimentAgent stub producing structured sentiment evidence.

    Returns fields:
    - sentiment descriptor
    - fear_greed_index
    - long_short_ratio
    - liquidations_24h
    """
    sentiment = random.choice(["extreme_greed", "greed", "neutral", "fear", "extreme_fear"]) 
    bias = "overlong" if sentiment in ("extreme_greed", "greed") else "balanced"

    fear_greed_index = int(random.uniform(10, 90))
    long_short_ratio = round(random.uniform(0.5, 3.0), 2)
    liquidations_24h = f"{int(random.uniform(0,500))}M"

    return {
        "sentiment": sentiment,
        "crowd_bias": bias,
        "fear_greed_index": fear_greed_index,
        "long_short_ratio": long_short_ratio,
        "liquidations_24h": liquidations_24h,
    }

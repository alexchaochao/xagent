"""Main CLI runner for prototype."""
from web3ai.collectors.binance_collector import fetch_ohlcv
from web3ai.agents.market_agent import analyze_market
from web3ai.agents.onchain_agent import analyze_onchain
from web3ai.agents.sentiment_agent import analyze_sentiment
from web3ai.decision_engine import decide
from web3ai.outputs.content_generator import generate_tweet, generate_youtube_script, generate_structured_report
from web3ai.outputs.telegram import send_telegram
from web3ai import config
import json


def run_once():
    print("Fetching klines from Binance...")
    df = fetch_ohlcv(symbol=config.BINANCE["symbol"], timeframe=config.BINANCE["timeframe"], limit=config.BINANCE["limit"])
    print(f"Fetched {len(df)} candles, last ts: {df.index[-1]}")

    market = analyze_market(df)
    onchain = analyze_onchain()
    sentiment = analyze_sentiment()

    decision = decide(market, onchain, sentiment)

    tweet = generate_tweet(decision, market, onchain, sentiment)
    yt = generate_youtube_script(decision, market, onchain, sentiment)

    # structured report
    report = generate_structured_report(config.BINANCE["symbol"], config.BINANCE["timeframe"], decision, market, onchain, sentiment)

    print("\n=== STRUCTURED REPORT (JSON) ===")
    print(json.dumps(report, indent=2))

    print("\n=== SIGNAL ===")
    print(decision)
    print("\n--- TWEET ---")
    print(tweet)
    print("\n--- YT SCRIPT ---")
    print(yt)

    # send to telegram if configured
    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
        msg = f"Signal: {decision['action']} (conf {decision['confidence']})\n{tweet}"
        ok = send_telegram(msg, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        print("Telegram sent:", ok)
    else:
        print("Telegram not configured - set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env to enable")

if __name__ == "__main__":
    run_once()

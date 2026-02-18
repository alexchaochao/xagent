import os
from dotenv import load_dotenv

load_dotenv()

# Use compact symbol for configs (e.g. BTCUSDT) and map later for ccxt
BINANCE = {
    "symbol": os.getenv("SYMBOL", "BTCUSDT"),
    "timeframe": os.getenv("TIMEFRAME", "4h"),
    "limit": int(os.getenv("LIMIT", "200")),
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Coinglass/Coingecko switches
COINGLASS_API_KEY = os.getenv("COINGLASS_API_KEY")
COINGECKO_ENABLED = os.getenv("COINGECKO_ENABLED", "true").lower() in ("1", "true", "yes")
COINGECKO_PREFERRED = os.getenv("COINGECKO_PREFERRED", "false").lower() in ("1", "true", "yes")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

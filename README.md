# Web3 AI Engine ¡ª Minimal Runnable Prototype

This repository contains a minimal, runnable prototype of the "Web3 AI Engine" architecture described by the user.

Quick start

1. Create a Python virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.sample` to `.env` and fill your keys (optional for Telegram):

```bash
cp .env.sample .env
```

3. Run the main script (one-shot):

```bash
python -m web3ai.cli.main
```

The prototype will fetch BTC klines from Binance (via `ccxt`), run three agents (market, onchain stub, sentiment stub), apply a simple decision rule, print signals and generate sample social content. If `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are provided in `.env`, it will attempt to send the signal to Telegram.

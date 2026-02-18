import os
import requests
from typing import Optional

def send_telegram(message: str, bot_token: Optional[str], chat_id: Optional[str]) -> bool:
    if not bot_token or not chat_id:
        print("Telegram not configured; skipping send")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        print("Failed to send Telegram message:", e)
        return False

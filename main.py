import requests
import threading
import time
from fastapi import FastAPI, Request

app = FastAPI()

TELEGRAM_TOKEN = "PUT_YOUR_TELEGRAM_TOKEN_HERE"
CHATGPT_KEY = "PUT_YOUR_OPENAI_KEY_HERE"

CHAT_ID = None

def send_telegram(msg):
    if CHAT_ID is None:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

@app.post("/webhook")
async def webhook(request: Request):
    global CHAT_ID
    data = await request.json()

    if "message" in data:
        CHAT_ID = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"]

        gpt = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {CHATGPT_KEY}"},
            json={
                "model": "gpt-5",
                "messages": [
                    {"role": "system", "content": "You are a trading assistant for MNTUSDT scalping signals."},
                    {"role": "user", "content": user_msg}
                ]
            }
        ).json()

        reply = gpt["choices"][0]["message"]["content"]
        send_telegram(reply)

    return {"ok": True}

def generate_signal():
    return "✅ MNTUSDT 5m Scalping Signal\nEntry: 3.64\nTP: 3.71\nSL: 3.58"

def auto_signal_loop():
    while True:
        time.sleep(300)  # every 5 minutes
        signal = generate_signal()
        send_telegram(signal)

threading.Thread(target=auto_signal_loop, daemon=True).start()


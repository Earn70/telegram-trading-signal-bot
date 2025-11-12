from fastapi import FastAPI, Request
import requests

BOT_TOKEN = "8307016683:AABEZvDQCj-ai8kUgKLFNmDcU6jL_MgOqJ"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bot is running fine."}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].lower()
        if text == "hi":
            requests.post(API_URL, json={"chat_id": chat_id, "text": "Hello 👋 MNTUSDT signal bot is active ✅"})
    return {"ok": True}

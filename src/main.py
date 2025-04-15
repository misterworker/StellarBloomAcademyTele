from fastapi import FastAPI, Request
from onboarding import handle_onboarding
from telegram import send_message
import asyncio

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    print("Payload: ", payload)
    # Inline button (callback_data)
    if "callback_query" in payload:
        query = payload["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        text = query["data"]
        username = query["from"]["first_name"]
    # Normal message
    elif "message" in payload:
        msg = payload["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text")
        username = msg["from"]["first_name"]
    else:
        return {"ok": True}

    response = await handle_onboarding(chat_id, text, username)
    print("Response: ", response)
    if response:
        await send_message(chat_id, response)

    return {"ok": True}

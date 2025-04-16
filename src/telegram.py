from dotenv import load_dotenv
import asyncio
import os
import httpx

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


async def send_message(chat_id, text, parse_mode="HTML"):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
            },
        )

async def send_chunked_message(chat_id, text, parse_mode="HTML", delay=1.5):
    chunks = [chunk.strip() for chunk in text.split("---") if chunk.strip()]

    for chunk in chunks:
        await send_typing_action(chat_id)
        await asyncio.sleep(delay)  # delay to simulate typing
        await send_message(chat_id, chunk, parse_mode=parse_mode)



async def send_message_with_buttons(chat_id, text, buttons, parse_mode="HTML"):
    """
    Sends a message with inline keyboard buttons.

    buttons: list of rows like:
    [
        [("Option A", "payload_a"), ("Option B", "payload_b")],  # Row 1
        [("Option C", "payload_c")]                              # Row 2
    ]
    """
    inline_keyboard = [
        [{"text": label, "callback_data": data} for (label, data) in row]
        for row in buttons
    ]

    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "reply_markup": {
                    "inline_keyboard": inline_keyboard,
                },
            },
        )

async def answer_callback_query(callback_query_id, text=None):
    """
    Optional: acknowledges a callback query if needed (e.g., to show a small popup).
    """
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BASE_URL}/answerCallbackQuery",
            json={
                "callback_query_id": callback_query_id,
                "text": text or "",
                "show_alert": False,
            },
        )

async def send_typing_action(chat_id):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BASE_URL}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
        )


import logging
import os

import httpx
from fastapi import FastAPI, Request

app = FastAPI()
logger = logging.getLogger(__name__)

FALLBACK_TEXT = "Обращайтесь! Рад был помочь!"


def _extract_message(update: dict) -> tuple[int | None, str | None]:
    message = update.get("message") or update.get("edited_message")
    if not message:
        return None, None
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text")
    return chat_id, text


async def _query_rag(question: str) -> str:
    rag_url = os.getenv("RAG_API_URL")
    if not rag_url:
        logger.error("RAG_API_URL is not set.")
        return FALLBACK_TEXT
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(rag_url, params={"question": question})
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer")
            return answer or FALLBACK_TEXT
    except Exception:
        logger.exception("RAG API request failed.")
        return FALLBACK_TEXT


async def _send_telegram_message(chat_id: int, text: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN is not set.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            await client.post(url, json=payload)
    except Exception:
        logger.exception("Telegram sendMessage failed.")


@app.post("/webhook")
async def telegram_webhook(request: Request) -> dict:
    update = await request.json()
    chat_id, text = _extract_message(update)
    if not chat_id:
        return {"ok": True}

    if not text:
        await _send_telegram_message(chat_id, FALLBACK_TEXT)
        return {"ok": True}

    answer = await _query_rag(text)
    await _send_telegram_message(chat_id, answer)
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8080)

# Telegram RAG Bot (FastAPI)

This service receives Telegram updates at `/webhook`, forwards message text to your
RAG API, and sends the `answer` back to the user. If there is no text or any error
occurs, it sends a polite fallback reply.

## Environment variables

- `TELEGRAM_BOT_TOKEN` - Telegram bot token
- `RAG_API_URL` - RAG query endpoint 

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="..."
export RAG_API_URL="..."
uvicorn server:app --host 0.0.0.0 --port 8080
```

## Set webhook

```bash
curl "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<my-bot-service>.up.railway.app/webhook"
```

## Docker

```bash
docker build -t telegram-rag-bot .
docker run -p 8080:8080 \
  -e TELEGRAM_BOT_TOKEN="..." \
  -e RAG_API_URL="..." \
  telegram-rag-bot
```

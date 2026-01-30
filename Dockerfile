FROM python:3.13-bookworm as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

FROM python:3.13-bookworm

WORKDIR /app
COPY --from=builder /install /usr/local
COPY server.py .

ENV PYTHONUNBUFFERED=1

EXPOSE 8080
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]

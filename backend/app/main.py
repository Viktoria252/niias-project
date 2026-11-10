import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="NIIAS Project API")

# Адрес Ollama внутри docker-сети
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

class QueryRequest(BaseModel):
    query: str
    limit: int = 3

@app.post("/api/ask")
async def ask_question(request: QueryRequest):
    # --- ЗАГЛУШКА ВМЕСТО RAG ---
    # Имитируем текст, который как будто бы нашелся в базе знаний
    stub_context = (
        "ИНСТРУКЦИЯ (ЗАГЛУШКА): При неисправности тормозов машинист обязан "
        "немедленно остановить поезд, зафиксировать инцидент в бумажном бланке "
        "и сообщить в диспетчерскую службу. При поломке локомотива - вызвать резерв."
    )
    # Имитируем список источников для фронтенда
    stub_sources = [
        "Тестовый документ 1 (Заглушка)",
        "Тестовый документ 2 (Заглушка)"
    ]

    # Формируем промпт для Qwen
    prompt = f"""Ты — ассистент диспетчера РЖД. Используй следующий контекст, чтобы ответить на вопрос.
Если в контексте нет ответа, скажи, что не знаешь.
Контекст:
{stub_context}

Вопрос: {request.query}
Ответ:"""

    # Отправляем запрос в Ollama (Qwen 2.5)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            },
            timeout=120.0  # Даем время на генерацию на CPU
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ошибка генерации ответа")

        answer = response.json()["response"]

    return {
        "answer": answer,
        "sources": stub_sources
    }
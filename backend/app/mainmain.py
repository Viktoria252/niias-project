# import os
# import httpx
# import lancedb
# import pandas as pd
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
#
# app = FastAPI(title="NIIAS Project API")
#
# # Адрес Ollama внутри docker-сети
# OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
# # Путь к базе данных (совпадает с томом в docker-compose)
# LANCEDB_PATH = "/app/data/lancedb"
#
# # Инициализация LanceDB при старте
# db = lancedb.connect(LANCEDB_PATH)
# # Создаем пустую таблицу, если ее нет (для теста)
# if "incidents" not in db.table_names():
#     db.create_table("incidents", data=[{"vector": [0.0] * 1024, "text": "init", "id": "0"}])
#
#
# class QueryRequest(BaseModel):
#     query: str
#     limit: int = 3
#
#
# async def get_embedding(text: str) -> list[float]:
#     """Получаем вектор текста через Ollama (модель BGE-M3)"""
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             f"{OLLAMA_HOST}/api/embeddings",
#             json={"model": "bge-m3", "prompt": text},
#             timeout=30.0
#         )
#         if response.status_code != 200:
#             raise HTTPException(status_code=500, detail="Ошибка получения эмбеддинга")
#         return response.json()["embedding"]
#
#
# @app.post("/api/ask")
# async def ask_question(request: QueryRequest):
#     # 1. Получаем эмбеддинг вопроса пользователя
#     query_vector = await get_embedding(request.query)
#
#     # 2. Ищем похожие документы в LanceDB
#     table = db.open_table("incidents")
#     # Ищем, исключая тестовую строку с id="0"
#     search_results = table.search(query_vector).limit(request.limit).to_pandas()
#
#     # Формируем контекст из найденных документов
#     context = "\n".join(search_results["text"].tolist())
#
#     # 3. Формируем промпт для Qwen
#     prompt = f"""
# Контекст:
# {context}
#
# Вопрос: {request.query}
# Ответ:"""
#
#     # 4. Отправляем запрос в Ollama (Qwen 2.5)
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             f"{OLLAMA_HOST}/api/generate",
#             json={
#                 "model": "qwen2.5:3b",
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {"temperature": 0.3}
#             },
#             timeout=120.0  # Даем время на генерацию на CPU
#         )
#
#         if response.status_code != 200:
#             raise HTTPException(status_code=500, detail="Ошибка генерации ответа")
#
#         answer = response.json()["response"]
#
#     return {
#         "answer": answer,
#         "sources": search_results["text"].tolist()
#     }
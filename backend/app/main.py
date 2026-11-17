import os
import httpx
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI(title="NIIAS Project API")

# Настройка базы данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:////app/data/applications.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель базы данных для заявки
class DBApplication(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, index=True)
    author = Column(String)
    loco_number = Column(String, nullable=True)
    failure_type = Column(String, nullable=True)
    description = Column(Text, nullable=True)

# Создаем таблицы при старте
Base.metadata.create_all(bind=engine)

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic схемы (для валидации данных от Vue)
class ApplicationCreate(BaseModel):
    number: str
    author: str
    loco_number: str = None
    failure_type: str = None
    description: str = None

class ApplicationResponse(ApplicationCreate):
    id: int
    class Config:
        from_attributes = True

# Маршруты API

@app.get("/api/applications", response_model=list[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(DBApplication).all()

@app.post("/api/applications", response_model=ApplicationResponse)
def create_application(app_data: ApplicationCreate, db: Session = Depends(get_db)):
    db_app = DBApplication(**app_data.model_dump())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@app.delete("/api/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    db_app = db.query(DBApplication).filter(DBApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    db.delete(db_app)
    db.commit()
    return {"message": "Удалено"}


# --- Новые маршруты для работы с конкретной заявкой ---

@app.get("/api/applications/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int, db: Session = Depends(get_db)):
    db_app = db.query(DBApplication).filter(DBApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return db_app


@app.put("/api/applications/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, app_data: ApplicationCreate, db: Session = Depends(get_db)):
    db_app = db.query(DBApplication).filter(DBApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    # Обновляем поля
    for key, value in app_data.model_dump().items():
        setattr(db_app, key, value)

    db.commit()
    db.refresh(db_app)
    return db_app

# --- Имитация анализа документа (ИИ) ---
@app.post("/api/analyze/{app_id}")
def analyze_document(app_id: int, db: Session = Depends(get_db)):
    # В реальности здесь будет загрузка файла, OCR и вызов Ollama/RAG
    # Сейчас мы просто имитируем, что ИИ нашел расхождения
    db_app = db.query(DBApplication).filter(DBApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    # Имитируем ответ от ИИ (в будущем здесь будет реальный вызов)
    # Допустим, ИИ "прочитал" документ и предложил свои варианты полей
    ai_results = {
        "loco_number": db_app.loco_number,  # Совпадает
        "failure_type": "Отказ датчика" if db_app.failure_type == "Сбой ПО" else db_app.failure_type,
        # Искусственно меняем для демонстрации
        "description": db_app.description  # Совпадает
    }

    return {"ai_data": ai_results}

# Заглушка RAG и Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

class QueryRequest(BaseModel):
    query: str
    limit: int = 3

@app.post("/api/ask")
async def ask_question(request: QueryRequest):
    stub_context = "ИНСТРУКЦИЯ (ЗАГЛУШКА): При неисправности тормозов машинист обязан немедленно остановить поезд, зафиксировать инцидент в бумажном бланке и сообщить в диспетчерскую службу."
    stub_sources = ["Тестовый документ 1 (Заглушка)", "Тестовый документ 2 (Заглушка)"]

    prompt = f"Ты — ассистент диспетчера РЖД. Используй контекст:\n{stub_context}\n\nВопрос: {request.query}\nОтвет:"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": "qwen2.5:3b", "prompt": prompt, "stream": False, "options": {"temperature": 0.3}},
            timeout=120.0
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ошибка генерации")
        answer = response.json()["response"]

    return {"answer": answer, "sources": stub_sources}
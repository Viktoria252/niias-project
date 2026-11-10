FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY ./app ./app

# Создаем папку для данных LanceDB
RUN mkdir -p /app/data/lancedb

# Запускаем Uvicorn (сервер)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
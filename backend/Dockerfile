FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
# Настраиваем pip на использование стабильного зеркала и увеличиваем таймауты
RUN pip config set global.index-url https://repo.huaweicloud.com/repository/pypi/simple && \
    pip config set global.timeout 120 && \
    pip config set global.retries 10

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY ./app ./app

# Создаем папку для данных LanceDB
RUN mkdir -p /app/data/lancedb

# Запускаем Uvicorn (сервер)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.13-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . /app

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Установка переменных окружения
ENV POSTGRES_HOST=127.0.0.1
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=videoscop
ENV MINIO_HOST=127.0.0.1
ENV MINIO_PORT=9000
ENV MINIO_USER=minioadmin
ENV MINIO_PASSWORD=minioadmin

# Команда для запуска приложения
CMD ["uvicorn", "backend.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]

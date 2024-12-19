# 1. Выбор базового образа
FROM python:3.10-slim

# 2. Установка рабочей директории
WORKDIR /app

# 3. Копируем файлы зависимостей проекта (poetry файлы)
COPY pyproject.toml poetry.lock ./

# 4. Устанавливаем poetry и зависимости проекта
RUN pip install poetry && poetry install --no-root

# 5. Копируем все файлы приложения в контейнер
COPY . .

# 6. Команда запуска FastAPI приложения через Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

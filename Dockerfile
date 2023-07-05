# Використовуємо офіційний базовий образ Python
FROM python:3.9-slim

# Встановлюємо Poetry
RUN pip install poetry

# Копіюємо файли проекту в контейнер
COPY . /app

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо залежності з файлу pyproject.toml
RUN poetry install --no-dev --no-interaction --no-ansi

# Відкриваємо порти
EXPOSE 3000
EXPOSE 5000

# Запускаємо HTTP сервер та Socket сервер
CMD ["poetry", "run", "python", "-u", "main.py"]
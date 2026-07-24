#!/bin/sh
set -e

# Готовим базу (миграции Alembic) перед стартом приложения.
# Postgres в docker-compose может подниматься чуть дольше бэкенда,
# поэтому повторяем попытки, пока база не станет доступна.
echo "Подготовка базы данных..."

attempt=1
max_attempts=15
until python prestart.py; do
  if [ "$attempt" -ge "$max_attempts" ]; then
    echo "Не удалось подготовить базу после $max_attempts попыток. Останавливаемся."
    exit 1
  fi
  echo "База ещё не готова (попытка $attempt/$max_attempts), ждём 3с..."
  attempt=$((attempt + 1))
  sleep 3
done

echo "Запускаем приложение."
exec uvicorn main:app --host 0.0.0.0 --port 8000

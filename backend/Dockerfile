FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# entrypoint применяет миграции Alembic, затем запускает uvicorn (без --reload
# для стабильности и скорости)
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/server

CMD sh -c "cd /app/server && alembic upgrade head && cd .. && python -m server.tests.db_init_filling && exec uvicorn server.src.main:app --host 0.0.0.0 --port 8000"

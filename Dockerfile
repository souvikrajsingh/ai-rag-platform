FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv

COPY . .

RUN uv pip install --system .

EXPOSE 10000

CMD ["sh", "-c", "exec uvicorn src.app.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
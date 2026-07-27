FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv

COPY . .

RUN uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "src.app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
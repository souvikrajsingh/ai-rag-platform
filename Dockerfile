FROM node:22-alpine AS frontend-build

WORKDIR /app/src/frontend
COPY src/frontend/package.json src/frontend/package-lock.json ./
RUN npm ci
COPY src/frontend/ ./
RUN npm run build

FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir uv

COPY . .
COPY --from=frontend-build /app/src/app/api/static/ ./src/app/api/static/

RUN uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "src.app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
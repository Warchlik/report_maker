FROM node:24-alpine AS node

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY ./frontend/ .

RUN npm run build

CMD ["tail", "-f", "/dev/null"]


FROM nginx:alpine AS nginx

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# COPY docker/fullchain.pem /etc/nginx/conf.d/fullchain.pem
# COPY docker/privkey.pem /etc/nginx/conf.d/privkey.pem

COPY --from=node /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]

# TODO: dokonczyć konfigurację builda pod pythona 
FROM python:3.13-slim as python

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  # uv: trzymaj venv poza kodem
  UV_PROJECT_ENVIRONMENT=/opt/venv \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

WORKDIR /app

# --- system deps (minimal + bezpieczne pod PDF/crypto) ---
# reportlab zwykle działa bez tego, ale te paczki zmniejszają ryzyko problemów z fontami/obrazami.
RUN apt-get update && apt-get install -y --no-install-recommends \
  ca-certificates \
  libfreetype6 \
  libjpeg62-turbo \
  zlib1g \
  && rm -rf /var/lib/apt/lists/*

# --- install uv (binarka) ---
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# --- deps: kopiuj tylko pliki zależności (dla cache) ---
COPY pyproject.toml uv.lock ./

# --- instalacja zależności z locka (deterministycznie) ---
RUN uv sync --frozen --no-dev

# --- kod aplikacji ---
COPY app ./app

# --- user non-root (bardziej "pro") ---
RUN useradd -m appuser && chown -R appuser:appuser /app /opt/venv
USER appuser

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

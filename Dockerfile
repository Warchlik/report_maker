FROM node:24-alpine AS node

WORKDIR /app

COPY ./frontend/package*.json ./
RUN npm install

COPY ./frontend/ .

RUN npm run build

CMD ["tail", "-f", "/dev/null"]


FROM nginx:alpine AS nginx

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./nginx/nginx-selfsigned.crt /etc/nginx/conf.d/nginx-selfsigned.crt
COPY ./nginx/nginx-selfsigned.key /etc/nginx/conf.d/nginx-selfsigned.key

COPY --from=node /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]



# TODO: dokonczyć konfigurację builda pod pythona 
FROM python:3.13-slim AS python

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_PROJECT_ENVIRONMENT=/opt/venv \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  ca-certificates \
  libfreetype6 \
  libjpeg62-turbo \
  zlib1g \
  && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY ./backend/pyproject.toml ./backend/uv.lock ./

RUN uv sync --frozen --no-dev

COPY ./backend/app/ ./app

RUN useradd -m appuser && chown -R appuser:appuser /app /opt/venv
USER appuser

ENV PATH="/opt/venv/bin:$PATH"



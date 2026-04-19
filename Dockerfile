# Dockerfile

FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000


CMD uv run python manage.py makemigrations && uv run python manage.py migrate && uv run python manage.py runserver 0.0.0.0:8000

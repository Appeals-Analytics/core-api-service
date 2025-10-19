FROM python:3.12-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --compile-bytecode --no-cache

COPY . .

FROM python:3.12-slim-trixie

RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app

COPY --from=builder /app/ ./

ENV PATH="/home/appuser/app/venv/bin:$PATH"

CMD ["uv", "run", "server"]
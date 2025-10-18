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

COPY --from=builder /app/.venv ./venv
COPY --from=builder /app/src ./src

ENV PATH="/home/appuser/app/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
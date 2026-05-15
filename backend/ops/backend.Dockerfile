FROM python:3.14

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY backend/ops/pyproject.toml backend/ops/uv.lock ./

RUN uv sync

COPY backend/ /app/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
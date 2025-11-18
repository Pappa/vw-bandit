FROM vowpalwabbit/vw-rel-alpine:9.9.0
FROM python:3.10-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data

# Install the local project into the system Python using uv
RUN uv pip install --system --no-cache-dir .



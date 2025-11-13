FROM vowpalwabbit/vw-rel-alpine:9.9.0
FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends \
    build-essential \
    ca-certificates && \
    update-ca-certificates

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src ./src

# Install the local project into the system Python using uv
RUN uv pip install --system --no-cache-dir .



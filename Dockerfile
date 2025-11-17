FROM vowpalwabbit/vw-rel-alpine:9.9.0
FROM python:3.10-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# RUN apt-get update && \
#     apt-get -y upgrade && \
#     apt-get -y install --no-install-recommends \
#     build-essential \
#     ca-certificates && \
#     update-ca-certificates

# Source - https://stackoverflow.com/a
# Posted by Marek
# Retrieved 2025-11-17, License - CC BY-SA 3.0


# Install Vowpal Wabbit dependencies
# RUN apt-get -y install \
#     libboost-dev \
#     libboost-program-options-dev \
#     libboost-system-dev \
#     libboost-math-dev \
#     libboost-thread-dev \
#     libboost-test-dev \
#     libboost-python-dev \
#     zlib1g-dev \
#     cmake

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data

# Install the local project into the system Python using uv
# RUN pip install setuptools
RUN uv pip install --system --no-cache-dir .



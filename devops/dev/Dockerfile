ARG BASE_IMAGE=python
ARG BASE_IMAGE_TAG=3.12-slim

FROM $BASE_IMAGE:$BASE_IMAGE_TAG AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install --no-cache-dir uv

WORKDIR /src
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --dev

# Copy application code
COPY . .

# Final stage
FROM $BASE_IMAGE:$BASE_IMAGE_TAG

# Create a non-root user
ARG USERNAME=appuser
ARG SCRIPTS_PATH=/src/devops/scripts
RUN useradd -m ${USERNAME}

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV in final stage
RUN pip install --no-cache-dir uv

WORKDIR /src
COPY --from=builder /src .
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Make entrypoint script executable
RUN chmod +x "/src/devops/scripts/entrypoint.sh"

# Set correct permissions
RUN chown -R ${USERNAME}:${USERNAME} /src && \
    chown -R ${USERNAME}:${USERNAME} /usr/local/lib/python3.12/site-packages && \
    chown -R ${USERNAME}:${USERNAME} /usr/local/bin

# Switch to non-root user
USER ${USERNAME}

# Use the entrypoint script
ENTRYPOINT ["/src/devops/scripts/entrypoint.sh"]

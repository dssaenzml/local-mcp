FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Copy only the files needed to resolve dependencies first
COPY pyproject.toml uv.lock README.md ./

# Install production dependencies inside a virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Copy application source
COPY src/local_mcp ./local_mcp

# -----------------------------------------------------------------------------
# Final runtime image – slim & secure
# -----------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Copy the pre-built virtual-env and the application code from the builder stage
COPY --from=builder /app /app

# Expose the venv to PATH and make the code importable
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app

# Default command executed by the container
ENTRYPOINT ["local-mcp"]
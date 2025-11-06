# Use a Python image with uv pre-installed (matches pyproject: >=3.13)
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Create non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

# uv settings
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install dependencies using lockfile (best layer caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy project and resolve local deps
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev

# Ensure venv is on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Flask defaults (override at runtime as needed)
ENV FLASK_APP=app:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
ENV FLASK_DEBUG=0
EXPOSE 8000

# Make app dir writable for SQLite, etc.
RUN chown -R nonroot:nonroot /app
USER nonroot

# Run the Flask app (switch to gunicorn for production)
CMD ["flask", "run", "--no-reload"]

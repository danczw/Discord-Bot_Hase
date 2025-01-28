# ---------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
WORKDIR /app

# copy only files for uv to create venv
COPY uv.lock .python-version pyproject.toml ./

# this will create the folder /app/.venv
RUN uv sync --frozen

# copy bot relevant files
COPY ./src/ ./
COPY ./logs/ ./logs/
COPY ./conf/ ./conf/
COPY ./data/ ./data/
RUN chmod 755 main.py

ENV ENV_DOCKER=True

# run bot
CMD ["uv", "run", "./main.py"]
# ---------------------------------------------------------------------
# build stage

FROM python:3.10-slim AS builder

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"

# install poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && chmod 755 ${POETRY_HOME}/bin/poetry

WORKDIR /app

# copy only pyproject.toml and poetry.lock file nothing else here
COPY poetry.lock pyproject.toml ./

# this will create the folder /app/.venv
RUN poetry install --no-dev --no-root --no-ansi --no-interaction

# ---------------------------------------------------------------------
# deployment stage

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    ENV_DOCKER="true" \
    DISCORD_TOKEN="discord" \
    OPENAI_API_KEY="openapi"

WORKDIR /app

# copy the venv folder from builder image 
COPY --from=builder /app/.venv ./.venv

COPY ./src/ ./
COPY ./logs/ ./logs/
COPY ./conf/ ./conf/
RUN chmod 755 bot.py

CMD ["python", "./bot.py"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]
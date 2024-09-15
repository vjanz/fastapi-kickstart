FROM python:3.12-alpine

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install build dependencies and Poetry
RUN apk add --no-cache gcc musl-dev python3-dev linux-headers \
    && pip install --no-cache-dir poetry

# Copy the dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies without dev packages
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the application source code
COPY ./src /app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


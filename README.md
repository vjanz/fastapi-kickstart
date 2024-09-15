# FastAPI-Kickstart Template :rocket:

This repository provides a template for quickly starting a project with FastAPI. It includes configuration for testing with SQLite, PostgreSQL integration, and basic CRUD operations with SQLAlchemy. This template is ideal for developers looking to kickstart their FastAPI projects with a solid foundation.

## Features :mag_right:

- **SQLAlchemy**: ORM for SQL databases.
- **SQLite for Testing**: In-memory SQLite database for testing.
- **PostgreSQL Integration**: Basic configuration for PostgreSQL.
- **Test Setup**: Fixtures for database setup with SQLite and teardown, celery and redis.
- **CRUD Operations**: Basic CRUD operations with SQLAlchemy.
- **Poetry**: Dependency management with Poetry.
- **Celery**: Asynchronous task queue for background tasks.
- **Separated Dockerfile for Development and Production**: Dockerfile for development and production environments.
- **Workflows**: GitHub Actions for CI (Testing and Linting).
- **Makefile**: Makefile for common commands.

## Getting Started :clipboard:

### Prerequisites :dart:

- Python 3.12+
- PostgreSQL
- SQLite
- Redis
- Docker & docker-compose

### Installation :inbox_tray:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/vjanz/fastapi-kickstart.git
    cd fastapi-kickstart
    ```

2. **Install dependencies using Poetry for local development:**

    ```bash
    poetry install
    ```

3. **cp .env.example .env and modify if you'd like.**

    ```bash
    ENVIRONMENT=local
    PROJECT_NAME=FastAPI-kickstart

    # Backend
    BACKEND_CORS_ORIGINS="http://localhost,http://localhost:5173,https://localhost"
    SECRET_KEY=verysecretkey

    # Postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    POSTGRES_DB=fastapi-kickstart
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres

    # Redis/Celery
    REDIS_HOST=redis
    REDIS_PORT=6379
    ```

### Running the Application :gear:

The recommended way to run the stack is with Docker Compose. The following command will start the FastAPI application, PostgreSQL, and Redis:

```bash
docker-compose up -d --build
# or with make
make up
```

### Running & Generating migrations :arrows_counterclockwise:

To run the migrations, use the following command:
```bash
docker compose run --rm backend alembic upgrade head
# or with make
make migrate
```

To generate a new migration, use the following command:
```bash
docker compose run --rm backend alembic revision --autogenerate -m "migration message"
# or with make
make revision message="migration message"
```

### Running the tests :white_check_mark:
To run the tests, use the following command:

Test without cov:
```bash
pytest src -v -s

# or with make

make test
```

Tests with cov:
```bash
pytest src -v -s --cov=src --cov-report=term-missing

# or with make

make test-cov
```

### Roadmap :construction:

- [ ] Add User model and CRUD operations
- [ ] Add JWT Authentication

### Contributing :handshake:

Contributions are welcome! Please feel free to submit a PR or open an issue if you encounter any problems.
If you'd please read the [Contributing Guidelines](CONTRIBUTING.md) before submitting your PR.

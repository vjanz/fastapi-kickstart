import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    """
    Parse and normalize CORS origins.

    Converts a comma-separated string or a list of CORS origins into a
    list of strings. If the input is a string that does not start with
    '[', it splits by commas. If the input is a list or already a list
    of strings, it returns it as-is.

    Args:
        v (Any): The CORS origins as a string or list.

    Returns:
        list[str] | str: A list of CORS origins or a single string if input is already in the correct format.

    Raises:
        ValueError: If the input is neither a string nor a list.
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and a .env file.

    This class is used to load and validate application settings, including
    CORS origins, database configurations, and environment-specific settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    PROJECT_NAME: str = "FastAPI Kickstart"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "fastapi-kickstart"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    ALGORITHM: str = "HS256"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_URL(self) -> str:
        """
        Compute the Redis URL.

        Constructs the Redis URL using Redis host and port.

        Returns:
            str: The Redis URL.
        """
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Compute the SQLAlchemy database URI.

        Constructs the database URI for SQLAlchemy using PostgresSQL connection
        details.

        Returns:
            PostgresDsn: The database URI for SQLAlchemy.
        """
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()

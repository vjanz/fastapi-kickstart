import os
from collections.abc import Generator
from typing import Any

import pytest
from celery import Celery
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.api.dependencies import get_db
from src.core.db import Base
from src.main import app
from src.tests.factories import item  # noqa

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """
    Fixture to set up the test environment.

    This fixture creates all database tables before the test session starts and drops them after the session ends.
    It also removes the test database file if it exists.

    Yields:
        None
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


def get_test_db() -> Generator[Session, None, None]:
    """
    Generator function to provide a SQLAlchemy session for testing.

    This function yields a database session and ensures it is closed after use.

    Yields:
        A SQLAlchemy session object.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    Fixture to provide a FastAPI test client.

    This fixture overrides the database dependency with a test database session and returns a FastAPI TestClient instance.

    Returns:
        A FastAPI TestClient instance.
    """
    app.dependency_overrides[get_db] = get_test_db
    return TestClient(app)


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    """
    Fixture to create a database session for testing purposes.

    This fixture yields a SQLAlchemy session object and ensures it is closed after use.

    Yields:
        A SQLAlchemy session object.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session")
def celery_config() -> dict[str, Any]:
    """
    Fixture for configuring Celery settings for testing.
    """
    return {
        "broker_url": "memory://",
        "result_backend": "memory://",
        "task_always_eager": True,
    }


@pytest.fixture(scope="session")
def celery_worker(celery_config: dict[str, Any]) -> Celery:
    """
    Fixture to start a Celery worker for testing.
    """
    from src.core.celery_config import celery_app

    celery_app.config_from_object(celery_config)
    return celery_app

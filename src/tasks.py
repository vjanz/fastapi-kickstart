from src.celery_config import celery_app


@celery_app.task  # type: ignore
def reverse(name: str) -> str:
    return name[::-1]

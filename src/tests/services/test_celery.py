from celery import Celery

from src.tasks import reverse


def test_celery_reverse_task(celery_worker: Celery) -> None:  # noqa: ARG001
    """
    Test the reverse task in Celery.

    Args:
        celery_worker: The Celery worker fixture.
    """
    result = reverse.delay("vjanz")
    assert result.get() == "znajv"

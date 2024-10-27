from celery import Celery

from src.core.config import settings

celery_app = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

# Import the tasks module to ensure the worker recognizes the tasks or add autodiscover_tasks to the Celery app.
from src.tasks import *  # noqa

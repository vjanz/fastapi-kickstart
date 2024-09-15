from typing import Any

from fastapi import APIRouter

from src.tasks import reverse

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_router.get("/")
def run_reverse_task(name: str) -> dict[str, Any]:
    """
    Run a celery task called reverse

    Args:
        name (str): The string to reverse

    Returns:
        dict[str, Any]: A dictionary containing the task_id and the status of the task
    """
    task = reverse.delay(name)
    return {"task_id": task.id, "status": "Task is running"}

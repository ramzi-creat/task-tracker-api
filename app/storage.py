import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional, List
from uuid import uuid4

from app.models.schemas import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

DATA_FILE = Path(__file__).resolve().parent.parent / "tasks.json"

_tasks: dict[str, TaskResponse] = {}


def _load_tasks() -> None:
    """Load tasks from the JSON data file into the in-memory store.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """
    if not DATA_FILE.exists():
        return
    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        raw = []
    _tasks.clear()
    for item in raw:
        try:
            task = TaskResponse.model_validate(item)
        except Exception:
            continue
        _tasks[task.id] = task


def _save_tasks() -> None:
    """Persist all tasks to the JSON data file.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """
    payload = [task.model_dump(mode="json") for task in _tasks.values()]
    DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# Load existing tasks from the JSON file on module initialization.
_load_tasks()


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and persist a new task in memory and to the JSON data file.

    Args:
        payload: The task data used to create the new task.

    Returns:
        TaskResponse: The newly created task with a generated id and persisted fields.

    Raises:
        None.
    """
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        completed=False,
        due_date=payload.due_date,
        tags=payload.tags or [],
    )
    _tasks[task.id] = task
    _save_tasks()
    return task


def get_all_tasks(status=None, priority=None, overdue: Optional[bool] = None, tag: Optional[str] = None) -> list[TaskResponse]:
    """Return stored tasks, optionally filtered by status, priority, overdue, or tag.

    Args:
        status: Optional status filter value.
        priority: Optional priority filter value.
        overdue: Optional boolean flag used to filter by overdue tasks.
        tag: Optional tag name used to match task tags.

    Returns:
        list[TaskResponse]: A list of task objects matching the supplied filters.

    Raises:
        None.
    """
    tasks = list(_tasks.values())
    if status is not None:
        normalized_status = TaskStatus.normalize(status)
        tasks = [task for task in tasks if task.status == normalized_status]
    if priority is not None:
        normalized_priority = TaskPriority.normalize(priority)
        tasks = [task for task in tasks if task.priority == normalized_priority]
    
    # Filter by overdue (due_date < today and not done/completed)
    if overdue is not None:
        today = date.today()
        if overdue:
            tasks = [
                task for task in tasks 
                if task.due_date and task.due_date < today and task.status != "Done"
            ]
        else:
            tasks = [
                task for task in tasks 
                if not (task.due_date and task.due_date < today and task.status != "Done")
            ]
            
    # Filter by specific tag
    if tag is not None:
        tag = tag.strip()
        if tag:
            tag_lower = tag.lower()
            tasks = [
                task for task in tasks 
                if task.tags and any(t.lower() == tag_lower for t in task.tags)
            ]

    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Return a stored task by its identifier.

    Args:
        task_id: The unique task identifier.

    Returns:
        Optional[TaskResponse]: The matching task, or None if no task exists.

    Raises:
        None.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Update an existing task with the provided fields.

    Args:
        task_id: The unique task identifier.
        payload: The fields to apply to the existing task.

    Returns:
        Optional[TaskResponse]: The updated task, or None if the task does not exist.

    Raises:
        None.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    updated_task = task.model_copy(update={**updates})
    _tasks[task_id] = updated_task
    _save_tasks()
    return updated_task


def delete_task(task_id: str) -> bool:
    """Remove a task from the in-memory store and the JSON data file.

    Args:
        task_id: The unique task identifier.

    Returns:
        bool: True if the task was removed, otherwise False.

    Raises:
        None.
    """
    if task_id in _tasks:
        del _tasks[task_id]
        _save_tasks()
        return True
    return False


def _reset() -> None:
    """Clear the in-memory store and remove the JSON data file.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """
    _tasks.clear()
    if DATA_FILE.exists():
        DATA_FILE.unlink()
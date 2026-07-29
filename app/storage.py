from datetime import date, datetime, timezone
from typing import Optional, List
from uuid import uuid4

from app.models.schemas import TaskCreate, TaskResponse, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
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
    return task


def get_all_tasks(status=None, priority=None, overdue: Optional[bool] = None, tag: Optional[str] = None) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    
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
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    updated_task = task.model_copy(update={**updates})
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()

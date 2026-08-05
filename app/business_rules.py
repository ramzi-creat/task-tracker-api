from fastapi import HTTPException, status
from app.models.schemas import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.TODO),
    (TaskStatus.DONE, TaskStatus.TODO),
    (TaskStatus.TODO, TaskStatus.TODO),
    (TaskStatus.IN_PROGRESS, TaskStatus.IN_PROGRESS),
    (TaskStatus.DONE, TaskStatus.DONE),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Validate that a status transition is allowed.

    Args:
        current: The task's current status.
        new: The requested status for the task.

    Returns:
        None: This function returns no value when the transition is valid.

    Raises:
        HTTPException: 422 if the requested transition is not allowed.
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )

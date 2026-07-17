from typing import Optional

from pydantic import ConfigDict

from app.models.schemas import TaskCreate, TaskResponse, TaskStatus, TaskUpdate


class TaskCreateCompat(TaskCreate):
    model_config = ConfigDict(extra="forbid")


class TaskUpdateCompat(TaskUpdate):
    model_config = ConfigDict(extra="forbid")


class TaskResponseCompat(TaskResponse):
    model_config = ConfigDict(extra="forbid")


TaskCreate = TaskCreateCompat
TaskUpdate = TaskUpdateCompat
TaskResponse = TaskResponseCompat
TaskStatus = TaskStatus


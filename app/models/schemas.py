from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from enum import Enum
from datetime import date
from typing import Optional, List


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

    @classmethod
    def normalize(cls, value):
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            return value

        normalized = value.strip().lower().replace("-", " ").replace("_", " ")
        mapping = {
            "todo": cls.TODO.value,
            "to do": cls.TODO.value,
            "in progress": cls.IN_PROGRESS.value,
            "inprogress": cls.IN_PROGRESS.value,
            "done": cls.DONE.value,
        }
        return mapping.get(normalized, value)


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskCreate(StrictBaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        return TaskStatus.normalize(value)

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty whitespace")
        return v

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str] = None
    completed: bool
    due_date: Optional[date] = None
    tags: List[str] = []


class HealthResponse(BaseModel):
    status: str
    timestamp: str

class TaskUpdate(StrictBaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    tags: Optional[List[str]] = None

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        if value is None:
            return value
        return TaskStatus.normalize(value)

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        return [str(tag).strip() for tag in v if str(tag).strip()]

class TaskCreate(StrictBaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: List[str] = Field(default_factory=list)

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        return TaskStatus.normalize(value)

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty whitespace")
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        return [str(tag).strip() for tag in v if str(tag).strip()]
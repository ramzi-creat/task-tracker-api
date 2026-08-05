from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from enum import Enum
from datetime import date


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

    @classmethod
    def normalize(cls, value):
        """Normalize a status-like value into a supported TaskStatus enum member.

        Args:
            value: A string or TaskStatus instance to normalize.

        Returns:
            TaskStatus | object: A TaskStatus member for recognized values, or the
                original input when no mapping exists.

        Raises:
            None.
        """
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

    @classmethod
    def normalize(cls, value):
        """Normalize a priority-like value into a supported TaskPriority enum member.

        Args:
            value: A string or TaskPriority instance to normalize.

        Returns:
            TaskPriority | object: A TaskPriority member for recognized values, or the
                original input when no mapping exists.

        Raises:
            None.
        """
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            return value

        normalized = value.strip().lower().replace("-", " ").replace("_", " ")
        mapping = {
            "low": cls.LOW.value,
            "medium": cls.MEDIUM.value,
            "high": cls.HIGH.value,
        }
        return mapping.get(normalized, value)


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


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
        """Normalize a status-like value before validation.

        Args:
            value: The incoming status value.

        Returns:
            TaskStatus | object: A TaskStatus member for recognized values, or the
                original input when no mapping exists.

        Raises:
            None.
        """
        return TaskStatus.normalize(value)

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace(cls, v: str) -> str:
        """Validate that a task title is not empty or whitespace.

        Args:
            v: The proposed title value.

        Returns:
            str: The validated title.

        Raises:
            ValueError: If the title is empty or whitespace.
        """
        if not v or not v.strip():
            raise ValueError("Title cannot be empty whitespace")
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        """Normalize tag input into a list of trimmed tag strings.

        Args:
            v: Tag input provided by the caller.

        Returns:
            list[str]: A list of trimmed tag strings.

        Raises:
            None.
        """
        if v is None:
            return []
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        return [str(tag).strip() for tag in v if str(tag).strip()]


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str] = None
    completed: bool
    due_date: Optional[date] = None
    tags: List[str] = Field(default_factory=list)


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

    @field_validator("title", mode="before")
    @classmethod
    def title_must_not_be_none_or_empty(cls, v):
        """Validate that an update title is not None or whitespace.

        Args:
            v: The proposed title value.

        Returns:
            str | None: The validated title, or None if the title is not provided.

        Raises:
            ValueError: If the title is None or whitespace.
        """
        if v is None:
            raise ValueError("Title cannot be null")
        if isinstance(v, str) and not v.strip():
            raise ValueError("Title cannot be empty whitespace")
        return v

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        """Normalize a status-like value before validation.

        Args:
            value: The incoming status value.

        Returns:
            TaskStatus | object: A TaskStatus member for recognized values, or the
                original input when no mapping exists.

        Raises:
            None.
        """
        if value is None:
            return value
        return TaskStatus.normalize(value)

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        """Normalize tag input into a list of trimmed tag strings.

        Args:
            v: Tag input provided by the caller.

        Returns:
            list[str] | None: A list of trimmed tag strings, or None if no tags were provided.

        Raises:
            None.
        """
        if v is None:
            return None
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        return [str(tag).strip() for tag in v if str(tag).strip()]
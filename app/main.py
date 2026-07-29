# main.py
from datetime import datetime, timezone
from typing import List, Optional
import importlib
from contextlib import asynccontextmanager

try:
    fastapi = importlib.import_module("fastapi")
    FastAPI = fastapi.FastAPI
    HTTPException = fastapi.HTTPException
    status = fastapi.status
except ImportError as exc:
    raise ImportError(
        "fastapi is required to run the Task Tracker API. Install it with 'pip install fastapi'."
    ) from exc

from app.business_rules import validate_status_transition
from app.config import APP_ENV, PORT
from app.models import HealthResponse, TaskCreate, TaskResponse, TaskUpdate
from app import storage, __version__
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    print(f"[startup] APP_ENV={APP_ENV} PORT={PORT}")
    yield
    # Shutdown actions (if any)


app = FastAPI(
    title="Task Tracker API",
    version=__version__,
    description="A learning-focused REST API built with FastAPI and JSON file storage.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/health", response_model=HealthResponse, status_code=200, tags=["Health"])
async def health_check() -> HealthResponse:
    """Returns the service status and the current UTC timestamp."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/version", status_code=200, tags=["Health"])
async def version_check():
    """Returns the package version."""
    return {"version": __version__}


# --- TASK TRACKER ROUTES ---

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


def _parse_bool_query_param(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid value for overdue query parameter; expected true or false",
    )


@app.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def get_all_tasks(
    status: Optional[str] = Query(None, description="Filter tasks by status"),
    priority: Optional[str] = Query(None, description="Filter tasks by priority"),
    tag: Optional[str] = Query(None, description="Filter tasks by tag"),
    overdue: Optional[str] = Query(None, description="Filter tasks by overdue status"),
):
    """Retrieve all tasks from the storage backend with optional filters."""
    return storage.get_all_tasks(
        status=status,
        priority=priority,
        tag=tag,
        overdue=_parse_bool_query_param(overdue),
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def patch_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    existing = storage.get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    updates = payload.model_dump(exclude_unset=True)

    if payload.status is not None:
        if existing.status == "In Progress" and payload.status == "ToDo":
            raise HTTPException(
                status_code=422,
                detail="Invalid status transition: Cannot move task from In Progress back to ToDo",
            )

        if existing.status != payload.status:
            validate_status_transition(existing.status, payload.status)
        elif len(updates) == 1:
            raise HTTPException(status_code=422, detail="Task already has this status")

    updated_task = storage.update_task(task_id, payload)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=f"Task with id {task_id} not found"
        )
    return updated_task


@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    existing_task = storage.get_task_by_id(task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    
    if payload.status is not None:
        if existing_task.status != payload.status:
            validate_status_transition(existing_task.status, payload.status)
    
    updated_task = storage.update_task(task_id, payload)
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
async def delete_task(task_id: str):
    """Delete a task from the storage backend."""
    success = storage.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return


if __name__ == "__main__":
    uvicorn = importlib.import_module("uvicorn")
    print(f"Starting Task Tracker API in '{APP_ENV}' mode on port {PORT}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)

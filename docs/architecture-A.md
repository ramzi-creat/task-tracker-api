# Task Tracker — Architecture (Strategy A: Minimal Context)

## What it does

The Task Tracker is a learning-focused REST API built with **FastAPI** and **JSON file storage** (`app/main.py:47`). It provides full task CRUD operations with strict validation, priority management, status normalization, due-date tracking, overdue filtering, and task tagging. A vanilla-JavaScript Kanban board (`frontend/index.html`) consumes the API to display tasks in To Do / In Progress / Done columns and supports drag-and-drop status changes.

Key capabilities (from `README.md` and `tests/test_tasks.py`):
- **Task CRUD**: Create, read, update (PATCH partial / PUT full), and delete tasks.
- **Due dates & overdue status**: Tasks with a `due_date` before today that are not `Done` are considered overdue (`app/storage.py:112-124`).
- **Tags & filtering**: Tasks carry multiple tags; the list endpoint filters by `status`, `priority`, `tag`, and `overdue` query parameters (`app/main.py:141-170`).
- **Status transitions**: Enforced via `app/business_rules.py`; invalid transitions return 422.
- **Health/version endpoints**: `GET /health` and `GET /version` (`app/main.py:65-103`).

## Data model

Defined in `app/models/schemas.py` using Pydantic v2.

### Enums
- **`TaskStatus`** (`schemas.py:7`): `ToDo`, `In Progress`, `Done`. Provides `normalize()` to map variants like `"to do"`, `"inprogress"`, `"todo"` to canonical values.
- **`TaskPriority`** (`schemas.py:42`): `Low`, `Medium`, `High`, with a matching `normalize()`.

### Schemas
- **`TaskCreate`** (`schemas.py:79`): `title` (required, 1–200 chars, non-whitespace), `description` (default `""`), `status` (default `ToDo`), `priority` (default `Medium`), `assignee`, `due_date`, `tags` (list, default `[]`). Uses `extra="forbid"` via `StrictBaseModel` and normalizes status/tags before validation.
- **`TaskResponse`** (`schemas.py:144`): adds `id` (UUID string) and `completed` (bool) to the create fields.
- **`TaskUpdate`** (`schemas.py:161`): all fields optional; `title` cannot be `None` or whitespace; status/tags normalized.
- **`HealthResponse`** (`schemas.py:156`): `status` and `timestamp`.

### Persistence
Tasks are stored in-memory in `app/storage.py` (`_tasks: dict[str, TaskResponse]`) and persisted to a JSON file at `tasks.json` (`DATA_FILE`, `storage.py:9`). On module import, `_load_tasks()` populates the in-memory store from the file (`storage.py:58`).

## Request flow when a user creates a task

1. **Client** sends `POST /tasks` with a JSON body (e.g. `{"title": "My task"}`).
2. **Route handler** `create_task` in `app/main.py:108-124` receives the payload typed as `TaskCreate`.
3. **Validation** — Pydantic validates/normalizes the payload: title non-empty, status/priority normalized, tags trimmed, unknown fields rejected (`extra="forbid"`).
4. **Storage** — `storage.add_task(payload)` (`storage.py:61-86`) builds a `TaskResponse` with a new `uuid4()` id, `completed=False`, and defaults; inserts it into `_tasks`.
5. **Persistence** — `_save_tasks()` (`storage.py:41-54`) serializes all tasks to `tasks.json` (indent=2, UTF-8).
6. **Response** — FastAPI returns the `TaskResponse` with HTTP `201 Created` (`status.HTTP_201_CREATED`).

## Key files

| File | Role |
|------|------|
| `app/main.py` | FastAPI app instance, CORS middleware, all route handlers, query-param parsing (`_parse_bool_query_param`). |
| `app/storage.py` | In-memory store + JSON file persistence; `add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`, `_reset`. |
| `app/models/schemas.py` | Pydantic models and enums; validation and normalization logic. |
| `app/business_rules.py` | `VALID_TRANSITIONS` set and `validate_status_transition()` enforcing allowed status changes. |
| `app/config.py` | Loads `PORT` and `APP_ENV` from environment via `python-dotenv`. |
| `app/__init__.py` | Marks package; defines `__version__ = "0.1.0"`. |
| `app/models/__init__.py` | Re-exports schemas for convenient imports. |
| `frontend/index.html` | Vanilla-JS Kanban board; fetches `http://localhost:8000/tasks`, renders columns, drag-and-drop PATCH, create/edit modal. |
| `tests/conftest.py` | `TestClient` fixture and autouse `_reset_storage` fixture. |
| `tests/test_tasks.py` | pytest suite covering CRUD, validation, transitions, filters, due dates, tags. |
| `.github/workflows/ci.yml` | CI: Python 3.11, installs `requirements.txt`, runs `pytest -v --tb=short`. |
| `requirements.txt` | `fastapi`, `uvicorn`, `python-dotenv`, `pydantic`, `pytest`, `httpx`. |

## Conventions

### Stack & tooling (from `AGENTS.md`, `CLAUDE.md`)
- Python 3.11, FastAPI, Pydantic v2, pytest + httpx, vanilla JavaScript frontend.
- Server: `uvicorn app.main:app --reload --port 8000`; Tests: `pytest -v`.

### Business rules (must not be violated)
- Status values are `ToDo`, `In Progress`, `Done`; priority values are `Low`, `Medium`, `High`.
- Valid transitions: `ToDo -> In Progress`, `In Progress -> Done`, `Done -> In Progress` (plus self-transitions in `VALID_TRANSITIONS`); invalid transitions return 422 (`business_rules.py:4-13`).
- `In Progress -> ToDo` is explicitly rejected in `main.py:220-224`.
- Title is required, trimmed, and non-empty; `null` title on update returns 422.
- Preserve existing API response shapes unless explicitly asked.

### Code style
- Google-style docstrings on public functions and route handlers (README "Recent Improvements").
- Pydantic `extra="forbid"` for strict request validation (`StrictBaseModel`).
- Status/priority/tag normalization centralized in enum `normalize()` methods and field validators.
- In-memory store + JSON file persistence; no database or authentication (per `AGENTS.md`/`CLAUDE.md`).
- Tests use an autouse `_reset_storage` fixture to isolate state between tests.
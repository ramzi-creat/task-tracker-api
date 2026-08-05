# Task Tracker — Architecture (Strategy B: Structured Context)

## What it does
A learning-focused REST API built with **FastAPI** and **JSON file storage**
(`app/main.py:47`). It exposes full task CRUD (create, read, update, delete),
strict validation, status/priority normalization, due-date tracking with overdue
filtering, and tagging. A vanilla-JavaScript Kanban board (`frontend/index.html`)
consumes the API to render To Do / In Progress / Done columns with drag-and-drop
status changes.

## Data model
Defined in `app/models/schemas.py` (Pydantic v2).

| Schema / Enum | Purpose |
|---|---|
| `TaskStatus` | `ToDo` / `In Progress` / `Done`; `normalize()` maps variants (`schemas.py:7`) |
| `TaskPriority` | `Low` / `Medium` / `High`; matching `normalize()` (`schemas.py:42`) |
| `TaskCreate` | title (1–200, non-whitespace), description, status, priority, assignee, due_date, tags; `extra="forbid"` (`schemas.py:79`) |
| `TaskResponse` | `TaskCreate` fields plus `id` (UUID) and `completed` (`schemas.py:144`) |
| `TaskUpdate` | All-optional partial update model (`schemas.py:161`) |
| `HealthResponse` | `status` + `timestamp` (`schemas.py:156`) |

**Persistence:** in-memory dict `_tasks` in `app/storage.py:11`, persisted to
`tasks.json` via `_save_tasks()` on every mutation; loaded into memory at module
import (`storage.py:58`).

## Request flow when a user creates a task
1. Client sends `POST /tasks` with JSON (`{"title": "My task"}`).
2. `create_task` handler receives the payload typed as `TaskCreate` (`main.py:108`).
3. Pydantic validates/normalizes: non-empty title, status/priority mapping,
   trimmed tags, unknown fields rejected.
4. `storage.add_task(payload)` (`storage.py:61`) builds a `TaskResponse` with a
   new `uuid4()` id, `completed=False`, defaults applied; inserts into `_tasks`.
5. `_save_tasks()` (`storage.py:41`) serializes all tasks to `tasks.json`.
6. FastAPI returns the saved `TaskResponse` with **201 Created**.

## Key files
| File | Role |
|---|---|
| `app/main.py` | FastAPI app, CORS, all routes (`/health`, `/version`, task CRUD), boolean query parsing. |
| `app/storage.py` | In-memory store + JSON persistence; filter logic for status/priority/tag/overdue. |
| `app/models/schemas.py` | Pydantic enums/models; validation and normalization. |
| `app/business_rules.py` | `VALID_TRANSITIONS` + `validate_status_transition()` enforcing allowed status changes. |
| `app/config.py` | `PORT` / `APP_ENV` from environment via python-dotenv. |
| `app/__init__.py` | Package marker; `__version__ = "0.1.0"`. |
| `app/models/__init__.py` | Re-exports schemas for convenient imports. |
| `frontend/index.html` | Vanilla-JS Kanban board consuming the API. |
| `tests/` | pytest suite; `conftest.py` resets storage between tests. |

## Conventions
- **Stack (AGENTS.md):** Python 3.11, FastAPI, Pydantic v2, pytest + httpx, vanilla JS.
  Server: `uvicorn app.main:app --reload`; Tests: `pytest -v`.
- Status values `ToDo`/`In Progress`/`Done`; priority values `Low`/`Medium`/`High`.
- Valid transitions enforced in `business_rules.py`; `In Progress -> ToDo` explicitly
  rejected (`main.py:220-224`); invalid transitions return 422.
- Strict request validation via `StrictBaseModel` (`extra="forbid"`); titles must be non-whitespace.
- Preserve existing API response shapes; no database or authentication.
- Google-style docstrings on public functions; normalization centralized in enum
  methods and field validators.
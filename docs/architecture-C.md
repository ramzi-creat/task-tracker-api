# Architecture C — Task Tracker API

## What it does

A learning-focused REST API for tracking tasks, built with FastAPI and backed by
JSON file storage. It exposes endpoints to create, list (with filters), fetch,
update (PATCH/PUT), and delete tasks, plus `/health` and `/version` endpoints.
CORS is enabled for a set of local frontend origins.

## Data model

The task model is represented by Pydantic schemas (`TaskCreate`, `TaskResponse`,
`TaskUpdate`) imported from `app.models.schemas`. The exact schema definitions
are **not visible from the files I read** (only their usage is).

From `storage.add_task`, a stored task carries these fields:

- `id` — generated UUID string
- `title`
- `description` (defaults to `""`)
- `status` (a `TaskStatus` value)
- `priority` (a `TaskPriority` value)
- `assignee`
- `completed` (defaults to `False`)
- `due_date`
- `tags` (defaults to `[]`)

`TaskStatus` and `TaskPriority` are enums imported from `app.models.schemas`;
their allowed values are **not visible from the files I read**, though
`storage.py` compares status against the string `"Done"` and `main.py` against
`"In Progress"` and `"ToDo"`.

## Request flow when a user creates a task

1. Client sends `POST /tasks` with a `TaskCreate` payload.
2. `main.create_task` validates the payload against `TaskCreate` and calls
   `storage.add_task(payload)`.
3. `storage.add_task` builds a `TaskResponse` with a new `uuid4` id, defaults
   for `description`, `completed`, and `tags`, and stores it in the in-memory
   `_tasks` dict keyed by id.
4. `_save_tasks()` writes the full task list to the JSON data file
   (`tasks.json`).
5. The new `TaskResponse` is returned with HTTP 201.

## Key files

- `app/main.py` — FastAPI app, routes, CORS, lifespan, request validation.
- `app/storage.py` — in-memory store (`_tasks`) plus JSON file persistence
  (`tasks.json`), and all task CRUD operations.
- `app/models/schemas.py` — Pydantic schemas and enums (imported, **not read**).
- `app/business_rules.py` — status transition validation (imported, **not read**).
- `app/config.py` — `APP_ENV` and `PORT` (imported, **not read**).

## Conventions

- Routes live in `app/main.py`; persistence lives in `app/storage.py`.
- Storage is an in-memory dict loaded from a JSON file at module import and
  saved on every mutation.
- Every public function/endpoint has a docstring with Args/Returns/Raises.
- Status transitions are validated before updates (PATCH and PUT).
- Query filters (`status`, `priority`, `tag`, `overdue`) are applied in
  `storage.get_all_tasks`; `overdue` is parsed to a boolean in `main.py`.
- Errors are raised as FastAPI `HTTPException` (404 for missing tasks, 422 for
  invalid transitions/booleans).
- The app runs via uvicorn on `0.0.0.0:PORT` with reload when run as `__main__`.
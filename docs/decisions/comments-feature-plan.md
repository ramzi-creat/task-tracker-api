# Comments Feature Plan

## Data Model

Follow the existing Pydantic v2 pattern in `app/models/schemas.py`:

- **`CommentCreate(StrictBaseModel)`** — mirrors `TaskCreate`:
  - `author: str = Field(..., min_length=1, max_length=100)` — required, 1–100 chars
  - `body: str = Field(..., min_length=1, max_length=2000)` — required, 1–2000 chars
  - Add a `field_validator` for `author`/`body` to reject whitespace-only strings, mirroring `title_must_not_be_whitespace` in `TaskCreate`.
  - `extra="forbid"` inherited from `StrictBaseModel` rejects unknown fields (same as `TaskCreate`).

- **`CommentResponse(BaseModel)`** — mirrors `TaskResponse`:
  - `id: str` — server-generated UUID (same as `TaskResponse.id`)
  - `task_id: str` — references the parent task
  - `author: str`
  - `body: str`
  - `created_at: datetime` — server-generated UTC timestamp

- **`CommentUpdate(StrictBaseModel)`** — mirrors `TaskUpdate` (optional fields):
  - `author: Optional[str] = Field(None, min_length=1, max_length=100)`
  - `body: Optional[str] = Field(None, min_length=1, max_length=2000)`

- Export new models from `app/models/__init__.py` alongside existing exports.

- **TODO (My Critique):**
  - [ ] Should `CommentResponse` use `StrictBaseModel` too, or plain `BaseModel` like `TaskResponse`?
  - [ ] Should `created_at` be `datetime` with `timezone.utc` enforced, or ISO string like `HealthResponse.timestamp`?
  - [ ] Should we add a `CommentListResponse` wrapper or return a plain `List[CommentResponse]`?

## API Routes

Follow the existing route pattern in `app/main.py` (routes defined directly in `main.py`, no separate route files):

- **`POST /tasks/{task_id}/comments`** → `201 Created`, `response_model=CommentResponse`
  - Mirrors `create_task` (201 + `response_model`).
  - First check `storage.get_task_by_id(task_id)`; if `None`, raise `HTTPException(404, f"Task with id {task_id} not found")` — same pattern as `get_task`.
  - Call `storage.add_comment(task_id, payload)`.

- **`GET /tasks/{task_id}/comments`** → `200 OK`, `response_model=List[CommentResponse]`
  - Mirrors `get_all_tasks` (returns a list).
  - Check task exists first (404 if not), then return `storage.get_comments_for_task(task_id)`.
  - Order by `created_at` ascending.

- **`GET /comments/{comment_id}`** → `200 OK`, `response_model=CommentResponse`
  - Mirrors `get_task` (404 if not found).

- **`PATCH /comments/{comment_id}`** → `200 OK`, `response_model=CommentResponse`
  - Mirrors `patch_task` (404 if not found, apply partial updates via `model_dump(exclude_unset=True)`).

- **`DELETE /comments/{comment_id}`** → `204 No Content`
  - Mirrors `delete_task` (404 if not found, return no body).

- **TODO (My Critique):**
  - [ ] Should we support `PUT /comments/{comment_id}` to mirror `update_task`?
  - [ ] Should comment routes live in `main.py` or be extracted to a new `app/routes/comments.py`?
  - [ ] Should `GET /tasks/{task_id}/comments` return 404 or an empty list when the task doesn't exist?
  - [ ] Should comments be deletable when the parent task is deleted (cascade)?

## Tests

Follow the existing pytest style in `tests/test_tasks.py` and `tests/conftest.py`:

- Reuse `client` and `created_task` fixtures from `conftest.py`.
- Add a `created_comment` fixture in `conftest.py` that creates a task + comment, mirroring `created_task`.

Test cases (mirroring existing task tests):

- **Create:**
  - `test_create_comment_valid_returns_201_with_full_body` — POST valid comment, assert 201, `id`, `task_id`, `author`, `body`, `created_at` present.
  - `test_create_comment_missing_author_returns_422`
  - `test_create_comment_blank_author_returns_422` (whitespace-only)
  - `test_create_comment_author_too_long_returns_422` (101 chars)
  - `test_create_comment_missing_body_returns_422`
  - `test_create_comment_blank_body_returns_422`
  - `test_create_comment_body_too_long_returns_422` (2001 chars)
  - `test_create_comment_unknown_field_returns_422` (extra field, mirrors `test_create_task_unknown_field_returns_422`)
  - `test_create_comment_task_not_found_returns_404`

- **List:**
  - `test_list_comments_empty_returns_200_and_empty_list`
  - `test_list_comments_returns_all_for_task` (multiple comments, verify ordering by `created_at`)
  - `test_list_comments_task_not_found_returns_404`

- **Get:**
  - `test_get_comment_by_id_returns_comment`
  - `test_get_comment_by_id_not_found_returns_404_with_detail`

- **Patch:**
  - `test_patch_comment_partial_update_keeps_other_fields`
  - `test_patch_comment_not_found_returns_404`
  - `test_patch_comment_blank_author_returns_422`

- **Delete:**
  - `test_delete_comment_returns_204_no_body`
  - `test_delete_comment_missing_returns_404`

- **Server-generated timestamp:**
  - `test_comment_created_at_is_server_generated_utc` — assert `created_at` is present, parseable as ISO datetime, and ends with `+00:00` or `Z`.

- **TODO (My Critique):**
  - [ ] Should we add a test that `created_at` cannot be supplied by the client (rejected via `extra="forbid"`)?
  - [ ] Should we test that comments are scoped per-task (comments for task A don't appear for task B)?
  - [ ] Should we add a test for the 100-char and 2000-char boundary (exactly at limit passes)?

## Frontend Changes

Follow the existing vanilla JS pattern in `frontend/index.html`:

- **Display comments** under each task card:
  - Add a "Comments" section/button on each `.task-card` that expands to show comments for that task.
  - Fetch comments via `GET /tasks/{task_id}/comments` when expanded.
  - Render each comment with `author`, `body`, and formatted `created_at`.

- **Add comment form:**
  - Add a small form (author + body textarea) in the expanded comment section.
  - POST via `POST /tasks/{task_id}/comments`.
  - Client-side validation mirroring server rules: author 1–100 chars, body 1–2000 chars, both required.
  - Reuse the existing `#error-message` div for error display (same pattern as `drop()`).

- **API URL handling:**
  - Current `API_URL = "http://localhost:8000/tasks"` — comment endpoints would be `${API_URL}/${taskId}/comments`.

- **TODO (My Critique):**
  - [ ] Should comments be shown inline on the card or in a separate modal?
  - [ ] Should we support editing/deleting comments from the UI, or read-only + create only?
  - [ ] Should the comment count be shown on the task card (e.g., "3 comments")?

## Migration or Storage Notes

Follow the existing JSON-file storage pattern in `app/storage.py`:

- **In-memory store:** Add `_comments: dict[str, CommentResponse]` alongside `_tasks`.
- **Persistence:** Add a second JSON file `comments.json` (sibling to `tasks.json`), or embed comments within `tasks.json`.
  - **Option A (separate file):** `_load_comments()` / `_save_comments()` mirroring `_load_tasks()` / `_save_tasks()`. Simpler, keeps task file unchanged.
  - **Option B (embedded):** Store comments inside each task object. Avoids a second file but changes `TaskResponse` shape (violates AGENTS.md "Preserve existing API response shapes").
  - **Recommendation:** Option A (separate `comments.json` file) to preserve existing task response shape.

- **New storage functions** (mirroring existing ones):
  - `add_comment(task_id, payload) -> CommentResponse` — generates `id` via `uuid4()` (same as `add_task`), sets `created_at = datetime.now(timezone.utc)`, verifies task exists.
  - `get_comments_for_task(task_id) -> list[CommentResponse]` — filters `_comments` by `task_id`, sorted by `created_at`.
  - `get_comment_by_id(comment_id) -> Optional[CommentResponse]`
  - `update_comment(comment_id, payload) -> Optional[CommentResponse]` — mirrors `update_task` using `model_copy(update=...)`.
  - `delete_comment(comment_id) -> bool` — mirrors `delete_task`.
  - `_reset()` — also clear `_comments` and remove `comments.json` (mirrors existing `_reset`).

- **Cascade behavior:** Decide whether deleting a task also deletes its comments. If yes, update `delete_task` to remove matching comments.

- **TODO (My Critique):**
  - [ ] Separate `comments.json` vs. embedding in `tasks.json` — confirm Option A is preferred.
  - [ ] Should `_reset()` clear comments too (needed for tests)?
  - [ ] Should deleting a task cascade-delete its comments, or orphan them?
  - [ ] Is there a need for an index/lookup structure on `task_id` for performance, or is a linear filter fine at this scale?

## Open Questions

- Should comments support editing/deleting, or is create + read sufficient for this feature?
- Should `created_at` be returned as ISO 8601 with timezone offset (`+00:00`) or as `Z` suffix?
- Should the frontend show comments inline on the card, in a modal, or in a separate detail view?
- Should there be a comment count on the task card?
- Should deleting a task cascade-delete its comments?
- Should comments be ordered oldest-first or newest-first by default?

## My Critique

- **TODO (My Critique):**
  - [ ] Add your critique of the data model choices here.
  - [ ] Add your critique of the API route design here.
  - [ ] Add your critique of the test coverage here.
  - [ ] Add your critique of the frontend approach here.
  - [ ] Add your critique of the storage/migration approach here.
  - [ ] Add any additional open questions or concerns here.

## Generic vs Repo-Grounded Codex Comparison
Biggest difference: TODO
Plan I would hand to a teammate: TODO
Where the generic plan was still useful: TODO
Where repo grounding mattered most: TODO

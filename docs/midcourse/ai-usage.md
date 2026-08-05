# AI Usage Log — Task Tracker API

## Purpose

This document records how AI assistance was used across the Task Tracker API project: what was generated, what I reviewed and changed, what was accepted or rejected, and how each AI contribution was verified. It complements the [prompt-log.md](prompt-log.md) (raw prompts), [reflection.md](reflection.md) (personal reflection), [copilot-claude-reflection.md](copilot-claude-reflection.md) (tool comparison), and [governance-retrospective.md](governance-retrospective.md) (risk classification).

## AI Tools Used

- **Cline** (this session) — used for code generation, review, documentation, and verification across the whole project.
- **Copilot Codex** — used for small, local edits (route tweaks, schema tweaks, test additions).
- **Claude Code** — used for cross-file design reasoning and documentation.

## What AI Generated and What I Did With It

| Area | File(s) | What AI Generated | My Review & Action | Status |
|---|---|---|---|---|
| Backend models & validators | `app/models/schemas.py` | `TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskStatus.normalize`, `TaskPriority.normalize`, title trimming, tag normalization, `StrictBaseModel` with `extra="forbid"`. | Reviewed every class and validator line by line. Added Google-style docstrings. Verified behavior against the pytest suite. | **Accepted** (with docstring additions) |
| Business rules | `app/business_rules.py` | `VALID_TRANSITIONS` frozenset and `validate_status_transition` raising 422 on invalid transitions. | Reviewed the transition table. **Found a contradiction:** `(IN_PROGRESS, TODO)` is listed as valid here, but `app/main.py:220-224` hardcodes a 422 rejection for it. Same-status transitions are also listed as valid here but rejected in the route. Logged as High/Medium findings in `docs/security-review.md`. | **Accepted with caveat** — contradiction flagged for resolution |
| Storage layer | `app/storage.py` | In-memory store with JSON file persistence, `add_task`, `get_all_tasks` (with status/priority/overdue/tag filters), `get_task_by_id`, `update_task`, `delete_task`, `_reset`. | Reviewed all functions. Confirmed overdue filter correctly excludes `status == "Done"` tasks (the AI's original assumption was corrected — see `user-stories.md`). | **Accepted** (with overdue-logic correction) |
| Route handlers | `app/main.py` | CRUD endpoints: `create_task`, `get_all_tasks`, `get_task`, `patch_task`, `update_task`, `delete_task`, plus `_parse_bool_query_param` helper and CORS middleware. | Reviewed all routes. Fixed the deprecated 422 status usage and the mutable-default-list pattern. **Found the hardcoded In Progress → ToDo block** that contradicts `business_rules.py`. Noted that `get_all_tasks` and `delete_task` are `async` with no `await` — I cannot confidently explain why. | **Accepted** (with findings logged) |
| Frontend board & drag-and-drop | `frontend/index.html` | Kanban board with three columns, HTML5 drag-and-drop, modal create/edit form, `fetch`/PATCH calls, priority badges. | Reviewed the render loop, drag events, and status normalization. Fixed the "To Do" ↔ "ToDo" mapping. **Found stored XSS** — `card.innerHTML` interpolates `task.title`/`task.description` without escaping (High severity, logged in security review). | **Accepted** (XSS logged as top backlog item) |
| CI workflow | `.github/workflows/ci.yml` | GitHub Actions workflow: checkout, setup-python, pip cache, install, pytest. | Reviewed every step. Added the pip-cache step. Noted actions are pinned to mutable tags (`@v4`/`@v5`) — logged as Medium finding. | **Accepted** (with cache addition) |
| Dockerfile | `Dockerfile` | Two-stage build (builder venv → slim runtime), non-root user, `/health` healthcheck, uvicorn CMD. | Reviewed the build. Confirmed non-root user and healthcheck. Noted data-persistence risk (`tasks.json` on ephemeral filesystem) — logged as Info finding. | **Accepted** |
| Security review | `docs/security-review.md` | AI findings table with severity, evidence, and suggested fixes. | Verified every finding against source code, filled in Grade/Reason columns, added 5 manual findings, documented reconciliation, and prioritized the top-3 backlog. | **Accepted** (with my manual findings added) |

## What I Rejected or Corrected

| AI Suggestion | Why I Rejected/Corrected It | Reference |
|---|---|---|
| Many-to-many `tags` database table | Over-engineered for the course scope; a string-list field is simpler and testable. | `mini-adr.md` |
| Overdue = `due_date < today` only | Completed tasks (`status == "Done"`) must never be flagged as overdue. | `user-stories.md` |
| Tag filtering case-sensitive exact match | Should be case-insensitive and match any tag in the normalized list. | `user-stories.md` |
| Background cron job to mark tasks overdue | Over-engineered; overdue is computed dynamically. | `mini-adr.md` |

## Verification Evidence

- **Test suite:** 28 tests pass (`python -m pytest -v --tb=short`), covering CRUD, validation, status transitions, due dates, overdue filtering, and tag filtering.
- **Break tests:** Temporarily broke the overdue logic and the tag filter parameter; tests failed as expected, then passed after restoration (`verification.md`).
- **Manual browser checks:** Due-date picker and overdue indicator verified in the Kanban UI (`verification.md`).
- **Security review:** Every AI finding cross-checked against source; the stored XSS and the transition-rule contradiction were confirmed by direct code inspection.

## Lessons Learned

1. **AI is a strong generator but a weak verifier.** The AI produced correct Pydantic date validation quickly, but its overdue assumption and its transition table both needed human correction.
2. **Always re-check AI logic against business rules.** The `(IN_PROGRESS, TODO)` contradiction between `business_rules.py` and `main.py` was only caught by reading both files side by side.
3. **Reject over-engineering.** The AI's database suggestion for tags was a scope violation; the string-list approach kept the project aligned with the course.
4. **Security review is a checkpoint, not documentation.** The stored XSS the AI surfaced is a real, high-severity issue that must be fixed before release, not just recorded.
5. **Match the tool to the task.** Fast assistants (Copilot Codex) excel at narrow edits; reasoning-oriented assistants (Claude Code) excel at cross-file design and documentation (`copilot-claude-reflection.md`).
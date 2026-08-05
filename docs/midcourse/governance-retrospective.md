# Governance Retrospective - AI-Assisted Coding

## What I Shared With AI

| Item | Module | Risk Level | Reason |
|---|---|---|---|
| Task Tracker code | 2-5 | Low | This is a toy/course project with no sensitive data — no credentials, secrets, PII, health, financial, or production data — and I am authorized to share it. |
| Test output and stack traces | 2-4 | Medium | Stack traces and test output reveal internal file paths and architecture notes, which the rubric explicitly classifies as Medium even though no secrets or real data are present. |
| Frontend code | 3 | Low | The frontend is part of the same toy course project with no sensitive data and no user data, so sharing it is Low risk. |
| Dockerfile and CI YAML | 4 | Low | These are public-facing build and CI configuration files for the toy project with no credentials or secrets embedded, so sharing them is Low risk. |
| Any real external data used by mistake | N/A | None (N/A) | No real external data was used — all data was synthetic in-project test fixtures — so there is no risk; had any real external data been shared it would be High per the rubric. |

## What I Received From AI

| Generated Thing | Module | Do I Understand It Line by Line? | Action |
|---|---|---|---|
| Backend models and validators | 2 | Yes | Reviewed every class and validator in `app/models/schemas.py` (`TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskStatus.normalize`, `TaskPriority.normalize`, title trimming, tag normalization). Kept them, added Google-style docstrings, and verified behavior against the full pytest suite (`verification.md`: 21 baseline + new tests all passing). |
| Frontend board and drag-and-drop logic | 3 | Yes | Reviewed the HTML5 drag events (`ondragstart`, `ondragover`, `ondrop`), the render loop, and `fetch`/PATCH calls in `frontend/index.html`. Kept the structure but fixed the frontend/backend status normalization ("To Do" ↔ "ToDo") and added the error banner for rejected transitions (e.g., ToDo → Done). Gap found: due-date UI is missing from the board — logged in the security/backlog review. |
| CI workflow | 4 | Yes | Reviewed every step in `.github/workflows/ci.yml` (checkout, setup-python, cache, install, pytest). Kept it and added the pip-cache step so dependency installation is cached across runs. |
| Dockerfile | 4 | Yes | Reviewed the two-stage build (builder venv → slim runtime), non-root user creation (`groupadd`/`useradd` uid 1000), `/health` healthcheck, and `uvicorn` CMD. Kept it as-is and validated it builds and the healthcheck resolves 200. |
| Security findings and plans | 5 | Yes | Verified every AI finding against the source code before grading. Found the AI's severity assessments accurate (stored XSS in `frontend/index.html:190-199`, CORS `"null"` origin, unpinned deps, mutable CI tags). **My verification also caught a critical contradiction the AI missed:** `app/business_rules.py:8` lists `(IN_PROGRESS, TODO)` as a valid transition, but `app/main.py:220-224` hardcodes a 422 rejection for it, and the same-status transitions in `app/business_rules.py:10-12` conflict with the route-level rejection at `app/main.py:226-229`. Both were recorded as High/Medium manual findings in the security review. |

## Reflection: What I Will Do Differently Going Forward

- **Verify before trusting:** The AI's assumption that overdue = `due_date < today` was corrected so completed tasks (`status == "Done"`) are never flagged as overdue. I will always re-check AI logic against business rules.
- **Reject over-engineering:** The AI suggested a many-to-many tags database table; I rejected it in favor of a string-list field per `mini-adr.md` to keep scope aligned with the course.
- **Security review before merge:** The AI surfaced the stored XSS in the frontend card renderer. I will treat AI-discovered vulnerabilities as review-checkpoints, not just documentation, before calling a feature done.
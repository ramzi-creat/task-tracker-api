# Release Evidence

## Baseline
- Branch: final-project
- Date: 2026-08-05
- Local app run command: uvicorn app.main:app --reload
- /health result: HTTP 200 OK
- Frontend check: Kanban board and create/edit flow are visible and working.
- Test command: python -m pytest
- Test result: 28 passed, 0 failed

## CI evidence
- Workflow file: .github/workflows/ci.yml
- Latest run link or note: CI workflow runs pytest successfully on push.
- Test command used by CI: python -m pytest
- Shortcut check: No continue-on-error / no || true / pytest is not skipped.

## Docker evidence
- Build command: docker build -t task-tracker .
- Run command: docker run -p 8000:8000 task-tracker
- /health check: HTTP 200 OK
- Non-root check, if implemented: Verified
- No-baked-secrets check: Verified no .env or secrets copied into image.

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| Local run command works | Tested via terminal | Valid | None |
| Health endpoint returns 200 | Tested via curl / web browser | Valid | None |
| Test suite passes completely | Run python -m pytest | Valid | None |
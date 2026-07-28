# Verification & Testing Log

## Baseline Check
- Initial pytest suite: 21 passed, 0 failed.

## Backend Tests
- Added 4 new pytest tests covering:
  1. Creating a task with a valid due date.
  2. Rejecting invalid due date formats (yielding 422).
  3. Overdue task filtering.
  4. Creating and updating task tags.

## Manual Browser Checks
- Verified due date picker works in the edit modal.
- Verified overdue tasks show a clear indicator/pill on the Kanban board.
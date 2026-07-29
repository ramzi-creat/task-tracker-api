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

## Break Test Evidence

### Break Test 1: Due Date Overdue Logic
* **Defect Introduced:** Temporarily changed the overdue condition logic in the backend model so it always returns `false`.
* **Test Result:** Ran `pytest`, and the test verifying overdue tasks failed as expected.
* **Restoration:** Reverted the logic back to correct code.
* **Final Result:** Re-ran `pytest`, and the test passed successfully.

### Break Test 2: Tag Filtering Query Parameter
* **Defect Introduced:** Temporarily changed the tag filter query parameter name in the router from `tag` to `wrong_tag`.
* **Test Result:** Ran `pytest`, and the tag filter endpoint test failed with a 422/404 error.
* **Restoration:** Restored the parameter back to `tag`.
* **Final Result:** Re-ran `pytest`, and the test suite passed successfully.
# AI Prompt Log - Mid-Course Project

## Feature 1: Due Dates & Overdue Filter
- **Prompt 1 (Weak):** "How do I add a due date to my FastAPI task tracker?"
  - *Rewritten Strong Prompt:* "How do I add an optional `due_date` field using Pydantic `date` validation in FastAPI, ensuring invalid date strings return a 422 error?"
  - *AI Output:* Suggested using `from datetime import date` and an optional field `due_date: Optional[date] = None` in the Pydantic schema.
  - *Action:* Accepted and integrated into `app/schemas.py`.
- **Prompt 2:** "What is the cleanest way to check if a task is overdue in Python?"
  - *AI Output:* Provided a comparison using `datetime.date.today() > task.due_date`.
  - *Action:* Accepted for both backend logic and filtering.
- **Prompt 3:** "How do I add an HTML date picker input and an overdue pill badge to the frontend HTML/JS?"
  - *AI Output:* Suggested `<input type="date">` in the modal form and a conditional CSS/JS badge render.
  - *Action:* Accepted and edited to match existing DOM element IDs.

## Feature 2: Task Tagging & Filtering
- **Prompt 1 (Weak):** "How do I add tags to tasks?"
  - *Rewritten Strong Prompt:* "How do I implement a list of string tags (`tags: List[str] = []`) in a Pydantic model and support tag-based query filtering in a FastAPI router endpoint?"
  - *AI Output:* Provided a FastAPI query parameter implementation using `tags: Optional[str] = Query(None)` and filtering list comprehension logic.
  - *Action:* Integrated into the router and data models.
- **Prompt 2:** "How do I let users select tags on the frontend interface?"
  - *AI Output:* Suggested text input or comma-separated tag input fields in the task form.
  - *Action:* Accepted and added to the frontend task creation/edit modal.
- **Prompt 3:** "The tag filter test is too weak because it only creates one task and checks if it returns. Add a negative test case that creates a second task with a different tag to ensure it gets correctly filtered out."
  - *AI Output:* Provided the updated test implementation using multiple tasks with different tags to ensure strict filtering validation.
  - *Action:* Accepted and integrated into `tests/test_tasks.py`.
- **Prompt 4:** "How should the tag filter behave when a task has multiple tags and the request targets one of them?"
  - *AI Output:* Recommended returning the task when any tag matches and ensuring unrelated tags do not cause false positives.
  - *Action:* Documented as the expected behavior and reflected in the strengthened test cases.
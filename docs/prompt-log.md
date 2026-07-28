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
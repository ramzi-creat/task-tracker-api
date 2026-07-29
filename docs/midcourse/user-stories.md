# User Stories - Mid-Course Project

## Feature 1: Due Dates + Overdue Filter
- **Story 1:** As a user, I want to assign a due date to a task when creating or updating it so that I can track deadlines.
  - *Acceptance Criteria:* 
    - The backend accepts an optional `due_date` field (ISO date format).
    - Invalid date formats return a 422 validation error.
    - The frontend modal includes a due date picker input.
- **Story 2:** As a user, I want to see a visual indicator or filter for overdue tasks so that I can prioritize urgent work.
  - *Acceptance Criteria:*
    - Tasks past their due date display an overdue pill/indicator on the Kanban UI.
    - An overdue filter option allows viewing only overdue tasks.
- **AI Assumption Corrected:** The original assumption was that overdue logic could be based only on the due date. That was corrected so overdue checks now require the task to be both past due and not completed, preventing completed tasks from appearing in overdue results.

## Feature 2: Task Tagging & Filtering
- **Story 1:** As a user, I want to add tags to my tasks so that I can categorize and group related work.
  - *Acceptance Criteria:*
    - The backend accepts a list of string tags (`tags`) on task creation/update.
    - Tags are correctly stored and returned in task responses.
- **Story 2:** As a user, I want to filter tasks by specific tags so that I can focus on a single category.
  - *Acceptance Criteria:*
    - The API supports query parameters to filter tasks by tag.
    - The UI allows selecting tags to filter the task list.
- **AI Assumption Corrected:** The original assumption was that tag filtering should be case-sensitive and only match an exact tag string. That was corrected so filtering is case-insensitive and matches tasks that include the requested tag within a normalized list of tags.

---

## AI Assumption & Correction Log
- **Feature 1 Assumption:** Initially, the AI assumed that filtering tasks by overdue status (`?overdue=true`) only needed to check if `due_date < today`, ignoring the task's completion status.
- **Feature 1 Correction:** I corrected this assumption because completed tasks (status `"Done"`) should never be flagged or returned as overdue, even if their past due date has passed. I updated the filtering logic to explicitly require `task.status != "Done"` alongside the date check.
- **Feature 2 Assumption:** Initially, the AI assumed tag filtering could rely on exact string matching with the original capitalization.
- **Feature 2 Correction:** I corrected this assumption so tag filtering is case-insensitive and returns all tasks containing the requested tag in a normalized tag list.
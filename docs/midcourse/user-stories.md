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

## Feature 2: Task Tagging & Filtering
- **Story 1:** As a user, I want to add tags to my tasks so that I can categorize and group related work.
  - *Acceptance Criteria:*
    - The backend accepts a list of string tags (`tags`) on task creation/update.
    - Tags are correctly stored and returned in task responses.
- **Story 2:** As a user, I want to filter tasks by specific tags so that I can focus on a single category.
  - *Acceptance Criteria:*
    - The API supports query parameters to filter tasks by tag.
    - The UI allows selecting tags to filter the task list.
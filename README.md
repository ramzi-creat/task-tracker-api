# Task Tracker API - Mid-Course & Final Project

A robust FastAPI task management application featuring priority management, status normalization, due date tracking, overdue filtering, and task tagging.

## Features
1. **Task CRUD Operations:** Create, read, update, and delete tasks with strict validation.
2. **Due Dates & Overdue Status:** Assign due dates to tasks and track overdue status automatically.
3. **Tags & Filtering:** Add multiple tags to tasks and filter them dynamically via query parameters.
4. **Robust Testing:** Comprehensive test suite built with `pytest`.

## Documentation
- [Technical note](docs/midcourse/technical-note.md)
- [Reflection note: Copilot Codex vs Claude Code](docs/midcourse/copilot-claude-reflection.md)

## Setup & Running the Project

### Recent Improvements
- Added Google-style docstrings to public functions and route handlers throughout the app package.
- Fixed deprecated FastAPI 422 status usage and removed the mutable default list pattern in the task response model.
- Verified the API behavior with the existing pytest suite.

### 1. Create a virtual environment and install dependencies

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
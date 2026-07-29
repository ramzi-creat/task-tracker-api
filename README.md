# Task Tracker API - Mid-Course Project

A robust FastAPI task management application featuring priority management, status normalization, due date tracking, overdue filtering, and task tagging.

## Features
1. **Task CRUD Operations:** Create, read, update, and delete tasks with strict validation.
2. **Due Dates & Overdue Status:** Assign due dates to tasks and track overdue status automatically.
3. **Tags & Filtering:** Add multiple tags to tasks and filter them dynamically via query parameters.
4. **Robust Testing:** Comprehensive test suite built with `pytest`.

## Setup & Running the Project

### 1. Create a virtual environment and install dependencies

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
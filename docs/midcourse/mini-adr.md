# Mini-ADR: Mid-Course Project Features

## Context and Problem Statement
We need to extend the Task Tracker API with two scoped features: (1) Due dates + overdue filter, and (2) Tags / labels, while maintaining a clean architecture and keeping the design simple.

## Decision Drivers
- Must fit within the existing FastAPI backend and frontend structure.
- Must support backend validation and frontend visibility.
- Keep implementation scope small and testable.

## Considered Options
1. **Due Dates:** 
   - *Option A:* Compute overdue status dynamically in the backend/UI. (Chosen)
   - *Option B:* Use a background cron job to update task statuses to 'overdue'. (Rejected as over-engineered for this scope).
2. **Tags/Labels:**
   - *Option C:* Store tags as a comma-separated string or list field with validation. (Chosen)
   - *Option D:* Create a separate many-to-many `tags` database table and relationship. (Rejected as unnecessary complexity for a simple task tracker extension).

## Decision
We will implement optional `due_date` validation with ISO date parsing and a simple tag management schema that integrates cleanly into the existing task creation, update, and Kanban UI components.
# AGENTS.md

## Task Tracker - Cline Instructions

This repository contains the Task Tracker API project. Follow the guidelines below when working on this codebase.

## Stack

- Python 3.11
- FastAPI
- Pydantic v2
- pytest
- Vanilla JavaScript frontend

## Run and test commands

- Server: `uvicorn app.main:app --reload`
- Tests: `pytest -v`

## Project rules

- Status values are ToDo, InProgress, Done.
- Priority values are Low, Medium, High.
- Preserve existing API response shapes unless explicitly asked.
- Do not add authentication or a database in Module 5.
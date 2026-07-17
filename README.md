# Task Tracker API

A simple RESTful API for creating, viewing, updating, and deleting tasks, built with Python and FastAPI. This is a learning project that uses in-memory storage (per ADR-001) rather than a database, keeping the setup minimal and easy to run locally.

## Setup

### 1. Create a virtual environment and install dependencies

**Linux/macOS (bash)**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and adjust values if needed:

**Linux/macOS**
```bash
cp .env.example .env
```

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env
```

## Running the Server

Start the server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, and interactive docs at `http://localhost:8000/docs`.

## Testing the Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok","timestamp":"2026-07-03T12:00:00.000000+00:00"}
```
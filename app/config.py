# config.py
# Loads application configuration from environment variables using
# python-dotenv. This centralizes settings so the rest of the app
# doesn't need to know how/where config values come from.

import os
from dotenv import load_dotenv  # type: ignore[import]

# Load variables from a .env file (if present) into the process environment.
# In production/deployment, real environment variables would take
# precedence since load_dotenv does not override existing ones by default.
load_dotenv()

# Port the Uvicorn server should run on. Defaults to 8000 if not set.
PORT: int = int(os.getenv("PORT", "8000"))

# Current application environment, e.g. "development" or "production".
# Used for informational/logging purposes only in this project.
APP_ENV: str = os.getenv("APP_ENV", "development")
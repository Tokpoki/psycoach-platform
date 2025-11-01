# PsyCoach

Modern sports-psychology companion composed of an Android client and a FastAPI backend.\
The app guides athletes through narrative scenarios, tracks progress, and integrates mini-games
while the backend provides authentication, content management, and persistence.

---

## Architecture

| Layer      | Stack & Responsibilities                                                        |
|------------|---------------------------------------------------------------------------------|
| Android    | Jetpack Compose, Hilt, Retrofit; handles UI, auth, navigation, mini-games.      |
| Backend    | FastAPI, SQLAlchemy, Alembic, Postgres; exposes REST API & business logic.      |
| Data store | PostgreSQL (dockerised) or SQLite (fallback for tests) via SQLAlchemy ORM.      |

---

## Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin)
- Java 17 + Android Studio (for the mobile app)
- PowerShell (commands below assume Windows host)

> ℹ️ The backend auto-runs Alembic migrations at startup, so a fresh database is prepared without manual steps.

---

## Quick Start (Docker)

1. Clone / unzip the repository and open PowerShell in the project root.
2. Start the database and API:
   ```powershell
   docker compose up -d db api
   ```
3. Seed demo data (admin user, scenarios, courses):
   ```powershell
   docker compose run --rm seed
   ```
   - Admin credentials: `admin@local` / `admin`
4. Verify the API:
   ```powershell
   Invoke-RestMethod `
     -Uri 'http://localhost:8000/ping' `
     -Method GET
   ```
5. Open the interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

Backend logs (watch in a separate shell):
```powershell
docker compose logs -f api
```

Stop services:
```powershell
docker compose down
```

---

## Android App

- The app points to `http://10.0.2.2:8000/` for emulator builds (default `API_BASE_URL`).
- For physical Android devices connected via USB:
  ```powershell
  adb reverse tcp:8000 tcp:8000
  ```
  then use `http://127.0.0.1:8000/` inside the app.
- iOS simulator (if porting the UI): use `http://127.0.0.1:8000/`; real devices require port forwarding (e.g. `iproxy 8000 8000`).

Registration requirements:
- Password ≥ 8 characters (`backend/app/schemas/auth.py`)
- Role must be one of: `athlete`, `coach`, `parent`, `psychologist`, `admin`

Common troubleshooting:
- `422 Unprocessable Entity`: usually means one of the fields is blank, role is misspelled, or password is too short.
- `400` with message about e-mail: the user already exists.
- Enable `docker compose logs -f api` to watch real-time validation errors.

---

## Backend Development Workflow

### Local environment (optional)

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The service reads configuration from `.env`. Sample values live in `.env.example`.

### Database migrations

- Migrations live under `backend/app/db/migrations`.
- On API startup we validate the schema; if the `users` table is missing, migrations run automatically.
- Manual commands (from repo root):
  ```powershell
  docker compose run --rm api alembic revision --autogenerate -m "message"
  docker compose run --rm api alembic upgrade head
  ```

### Seeding

```powershell
docker compose run --rm seed
```
Creates admin account, sample scenarios, lessons, and progress records.

---

## Testing & Quality

Run tests (currently none defined, command returns “no tests ran”):
```powershell
docker compose run --rm api pytest
```

Static analysis:
```powershell
docker compose run --rm api ruff check
docker compose run --rm api black --check .
docker compose run --rm api isort --check-only .
docker compose run --rm api mypy --config-file mypy.ini backend/app
```

Pre-commit hooks:
```powershell
pre-commit install
pre-commit run --all-files
```

---

## Troubleshooting Checklist

- **Registration still fails**  
  - Confirm the API container is up (`docker compose ps`) and `http://localhost:8000/ping` returns `{ "message": "pong" }`.  
  - Watch `docker compose logs -f api` while performing the action; errors are logged with a stack trace.  
  - Ensure the database volume isn’t corrupted. For a clean slate stop the stack, delete the `postgres_data` volume, and rerun `docker compose up -d db api`.

- **Seeding fails with enum errors**  
  - Ensure you are on the latest code; enums now use `values_callable` so they serialize correctly.  
  - Rebuild images after dependency changes: `docker compose build --no-cache`.

---

## Project Structure

```
backend/
  app/
    api/          # FastAPI routers (auth, scenarios, progress, etc.)
    core/         # Settings, logging, database bootstrap
    db/           # Session factory, Alembic migrations, seed script
    models/       # SQLAlchemy domain models
    schemas/      # Pydantic request/response models
    services/     # Business logic helpers
android/
  app/            # Android module with Jetpack Compose UI and data layer
docs/             # Architectural notes & assets
tests/            # Placeholder for backend tests
```

---

## Useful Commands (Windows)

```powershell
# Ping the API
curl.exe http://localhost:8000/ping

# Register a new user
Invoke-RestMethod `
  -Uri 'http://localhost:8000/auth/register' `
  -Method POST `
  -ContentType 'application/json' `
  -Body (@{ email='demo@example.com'; password='Pass1234'; role='athlete' } | ConvertTo-Json)

# Login
Invoke-RestMethod `
  -Uri 'http://localhost:8000/auth/login' `
  -Method POST `
  -ContentType 'application/json' `
  -Body (@{ email='demo@example.com'; password='Pass1234' } | ConvertTo-Json)
```

---

## Status

- ✅ Backend migrations self-heal on startup.
- ✅ Database seed script succeeds (admin user + content).
- ✅ Registration tested via PowerShell; backend returns bearer token.
- ⚠️ Automated tests not yet implemented (pytest reports “no tests ran”).

Contributions welcome—add tests under `backend/tests/`, expand the Android experience, or integrate additional training content.

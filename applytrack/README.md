# ApplyTrack — Job Application Tracker

A full-stack application for organizing working-student, internship and graduate-role applications. It demonstrates a typed REST API, JWT authentication, relational persistence, a React dashboard and containerized local development.

## Problem and scope
Job searches create scattered notes and inconsistent follow-ups. ApplyTrack stores each application, its pipeline status and notes in one personal workspace. This is a portfolio/demo application, not a production multi-tenant SaaS.

## Architecture
```mermaid
flowchart LR
  U[Browser] --> W[React + Vite]
  W -->|JSON + Bearer JWT| A[FastAPI]
  A --> D[(PostgreSQL)]
  A --> H[/health]
```

## Tech stack
- Frontend: React 19, TypeScript, Vite
- Backend: Python 3.12, FastAPI, SQLAlchemy, Pydantic
- Database: PostgreSQL 16; SQLite for isolated tests
- Security: bcrypt password hashing and signed JWT access tokens
- Quality: pytest, Ruff, GitHub Actions
- Runtime: Docker Compose

## Run locally
1. Install Docker Desktop / Docker Engine with Compose v2.
2. Copy `.env.example` to `.env`; replace `POSTGRES_PASSWORD` and `JWT_SECRET` for your local environment.
3. Run `docker compose up --build`.
4. Open http://localhost:5173. Register an account and add applications.
5. Open http://localhost:8000/docs for interactive OpenAPI documentation.

Without Docker, install `backend/requirements.txt`, set `DATABASE_URL=sqlite:///./applytrack.db`, run `uvicorn app.main:app --app-dir backend --reload`, and separately run `npm install && npm run dev` in `frontend`.

## Tests
```bash
cd backend
python -m pip install -r requirements.txt
ruff check app tests
pytest -q
```
Tests use SQLite and do not need a running PostgreSQL server.

## API overview
- `POST /auth/register`, `POST /auth/login`
- `GET/POST /applications`
- `GET/PATCH/DELETE /applications/{id}`
- `GET /applications/statistics`
- `GET /health`
- OpenAPI: `/docs`, `/openapi.json`

## Decisions and assumptions
- A single account owns its applications; every query is scoped by the authenticated user ID.
- Pipeline statuses are `saved`, `applied`, `interview`, `offer`, and `rejected`.
- The dashboard is intentionally compact to keep the project understandable.
- Schema creation uses SQLAlchemy `create_all` for a small demo. A production service should use Alembic migrations.
- The JWT secret and database password have safe-to-notice local defaults only; configure strong values before any deployment.

## Limitations
- No password reset, email verification, refresh-token rotation, rate limiting or audit log.
- No pagination yet; no production migration strategy.
- Frontend stores the access token in localStorage, which is vulnerable to token theft if an XSS bug is introduced.
- No live hosted service is provisioned.

## What I would improve
- Add Alembic migrations, refresh-token rotation and password reset.
- Add pagination, search, reminders and CSV export.
- Add frontend component tests and end-to-end Playwright tests.
- Add accessibility review, structured logs and deployment secrets management.

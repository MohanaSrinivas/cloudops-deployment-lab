# Local operations runbook
- `docker compose ps`: inspect service state.
- `docker compose logs -f api`: follow API logs.
- `docker compose restart api`: restart the API.
- `curl -fsS http://localhost:8000/health`: API liveness check.
- `docker compose down`: stop services without deleting named volumes.
- `docker compose down -v`: destructive reset of local data.

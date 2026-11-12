#!/usr/bin/env bash
set -euo pipefail
docker compose config --quiet
docker compose up --build -d
cleanup() { docker compose down -v; }
trap cleanup EXIT
for i in $(seq 1 30); do
  if curl -fsS http://localhost:8000/health >/dev/null; then break; fi
  sleep 2
done
curl -fsS http://localhost:8000/health

# Phase 01: Project Skeleton

## Branch

```text
phase/01-project-skeleton
```

## Goal

Create the runnable application shell: backend, frontend, Docker Compose, and health checks.

## Scope

- Add `backend/` FastAPI app with a `/health` endpoint.
- Add `frontend/` React + TypeScript app shell.
- Add Docker Compose for PostgreSQL and Qdrant.
- Add backend configuration loading.
- Add basic local run documentation.

## Suggested Commits

```text
add fastapi application skeleton
add react dashboard shell
add docker compose for postgres and qdrant
document local startup commands
```

## Files To Add Or Update

```text
backend/app/main.py
backend/app/core/config.py
backend/requirements.txt
frontend/src/App.tsx
frontend/package.json
docker-compose.yml
README.md
```

## Acceptance Criteria

- Backend starts locally.
- `GET /health` returns a healthy response.
- Frontend starts locally and renders an app shell.
- PostgreSQL and Qdrant containers start through Docker Compose.

## Verification

```bash
docker compose up -d postgres qdrant
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

## Push Plan

```bash
git switch main
git pull
git switch -c phase/01-project-skeleton
git push -u origin phase/01-project-skeleton
```


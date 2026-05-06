# Phase 07: Evals, CI, And Polish

## Branch

```text
phase/07-evals-ci-polish
```

## Goal

Make the project feel production-style and ready to show: tests, evals, CI, structured logs, and final demo commands.

## Scope

- Add RAG evaluation questions.
- Add agent workflow evaluation cases.
- Add structured request and tool-call logging.
- Add GitHub Actions CI.
- Add demo commands and screenshots if useful.
- Tighten README setup, architecture, and demo sections.

## Suggested Commits

```text
add rag evaluation dataset
add agent workflow evals
add structured application logging
add github actions ci
document end to end demo flow
```

## Files To Add Or Update

```text
backend/app/evals/rag_eval.py
backend/app/evals/agent_eval.py
backend/app/evals/test_questions.json
backend/app/core/logging.py
.github/workflows/ci.yml
README.md
```

## Acceptance Criteria

- Backend tests run in CI.
- Frontend build runs in CI.
- RAG and agent eval scripts run locally.
- README includes clear setup and demo instructions.
- Final branch produces a complete MVP demo.

## Verification

```bash
cd backend && pytest
cd frontend && npm run build
```

## Push Plan

```bash
git switch main
git pull
git switch -c phase/07-evals-ci-polish
git push -u origin phase/07-evals-ci-polish
```


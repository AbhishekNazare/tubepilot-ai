# TubePilot AI Phase Plan

This folder turns the product README into an implementation sequence that creates a clean GitHub history. Each phase should be a focused branch and pull request that can stand on its own.

## Repository Rules

- Work from `main`.
- Create one branch per phase using the exact branch names below.
- Keep each commit focused on one behavior or structural milestone.
- Push the branch after each meaningful commit group.
- Open a PR for each phase with the phase checklist in the PR body.
- Merge only after the acceptance criteria and verification steps pass.
- Avoid mixing future-phase work into an earlier phase.

## Branch Sequence

| Phase | Branch | Outcome |
| --- | --- | --- |
| 00 | `phase/00-repo-foundation` | Repository, docs, environment conventions |
| 01 | `phase/01-project-skeleton` | FastAPI, React, Docker Compose skeleton |
| 02 | `phase/02-synthetic-data` | Synthetic analytics data and database seed |
| 03 | `phase/03-risk-predictor` | Baseline ML risk model and prediction API |
| 04 | `phase/04-rag-pipeline` | Document ingestion, chunking, embeddings, retrieval |
| 05 | `phase/05-agent-orchestrator` | Tool-calling agent workflow and timeline persistence |
| 06 | `phase/06-react-dashboard` | Demo-ready dashboard pages |
| 07 | `phase/07-evals-ci-polish` | Tests, evals, logs, CI, final demo polish |

## Commit Style

Use imperative, behavior-focused commit messages:

```text
add fastapi health endpoint
define postgres analytics schema
seed synthetic youtube metrics
train baseline video risk model
index creator strategy documents
persist agent tool timeline
connect ask ai page to chat api
add ci workflow for backend tests
```

Avoid vague messages such as `updates`, `fix stuff`, or `wip`.

## PR Template

```md
## Phase

Phase XX: Name

## What Changed

- ...

## Verification

- [ ] ...

## Notes

- ...
```


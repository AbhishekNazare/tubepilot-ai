# Phase 02: Synthetic Analytics Data

## Branch

```text
phase/02-synthetic-data
```

## Goal

Create realistic YouTube-style analytics data so the MVP works without YouTube API credentials.

## Scope

- Define PostgreSQL tables for channels, videos, video metrics, and channel metrics.
- Generate synthetic CSV data.
- Add a seed script.
- Add repository docs that explain the generated data assumptions.
- Add basic tests for data shape and seed behavior.

## Suggested Commits

```text
define analytics database schema
generate synthetic youtube analytics csvs
add postgres seed script
test synthetic data loading
```

## Files To Add Or Update

```text
backend/app/db/models.py
backend/app/db/session.py
backend/app/db/seed.py
data/channels.csv
data/videos.csv
data/video_metrics_daily.csv
backend/tests/test_seed_data.py
README.md
```

## Acceptance Criteria

- Database schema matches the README model.
- Seed command inserts repeatable demo data.
- Data includes enough variation for risk prediction.
- Tests validate required columns and basic relationships.

## Verification

```bash
docker compose up -d postgres
cd backend && pytest tests/test_seed_data.py
```

## Push Plan

```bash
git switch main
git pull
git switch -c phase/02-synthetic-data
git push -u origin phase/02-synthetic-data
```


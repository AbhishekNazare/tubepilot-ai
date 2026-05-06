# Phase 03: Video Risk Predictor

## Branch

```text
phase/03-risk-predictor
```

## Goal

Train and serve a baseline model that predicts whether a video is likely to underperform.

## Scope

- Add feature engineering for video-level analytics.
- Create underperformance labels from channel-relative performance.
- Train a baseline scikit-learn model.
- Save model artifacts with joblib.
- Add `POST /predictions/video-risk`.
- Persist prediction outputs to PostgreSQL.

## Suggested Commits

```text
add video risk feature engineering
train baseline underperformance model
serve video risk prediction endpoint
persist prediction results
test prediction service
```

## Files To Add Or Update

```text
backend/app/ml/features.py
backend/app/ml/train.py
backend/app/ml/predict.py
backend/app/ml/model_registry.py
backend/app/api/predictions.py
models/video_risk_model.joblib generated locally
backend/tests/test_predictions.py
```

## Acceptance Criteria

- Training script runs from seeded data.
- Prediction API returns `risk_score`, `risk_level`, and `top_factors`.
- Risk levels are deterministic for the same model and input data.
- Tests cover low, medium, and high-risk examples.

## Verification

```bash
cd backend && python -m app.ml.train
cd backend && pytest tests/test_predictions.py
```

## Push Plan

```bash
git switch main
git pull
git switch -c phase/03-risk-predictor
git push -u origin phase/03-risk-predictor
```

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models import Prediction
from app.ml.features import FEATURE_NAMES, build_video_feature_row
from app.ml.model_registry import MODEL_PATH, load_model


@dataclass(frozen=True)
class VideoRiskPrediction:
    video_id: str
    risk_score: float
    risk_level: str
    top_factors: list[str]


def _risk_level(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def _top_factors(features: dict[str, float]) -> list[str]:
    candidates: list[tuple[str, float]] = [
        ("low_ctr", abs(min(features["ctr_delta"], 0.0))),
        ("low_retention", abs(min(features["retention_delta"], 0.0)) / 4.0),
        ("low_views_vs_channel_average", abs(min(features["view_ratio"] - 1.0, 0.0)) * 4.0),
        ("negative_subscriber_delta", 2.0 if features["subscriber_delta"] < 100 else 0.0),
        ("low_average_view_duration", 1.0 if features["avg_view_duration"] < 260 else 0.0),
    ]
    ranked = [name for name, score in sorted(candidates, key=lambda item: item[1], reverse=True) if score > 0]
    return ranked[:3] or ["healthy_metric_profile"]


def predict_video_risk(
    session: Session,
    video_id: str,
    model_path: Path = MODEL_PATH,
    persist: bool = True,
) -> VideoRiskPrediction:
    artifact = load_model(model_path)
    row = build_video_feature_row(session, video_id)
    feature_vector = [[row.features[name] for name in FEATURE_NAMES]]
    risk_score = float(artifact.model.predict_proba(feature_vector)[0][1])
    prediction = VideoRiskPrediction(
        video_id=video_id,
        risk_score=round(risk_score, 4),
        risk_level=_risk_level(risk_score),
        top_factors=_top_factors(row.features),
    )

    if persist:
        session.add(
            Prediction(
                prediction_id=f"pred_{uuid4().hex[:12]}",
                video_id=video_id,
                risk_score=prediction.risk_score,
                risk_level=prediction.risk_level,
                top_factors=json.dumps(prediction.top_factors),
                created_at=datetime.utcnow(),
            )
        )
        session.commit()

    return prediction


from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib

from app.ml.features import FEATURE_NAMES

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "video_risk_model.joblib"


@dataclass(frozen=True)
class ModelArtifact:
    model: Any
    feature_names: list[str]
    metrics: dict[str, float]


def save_model(model: Any, metrics: dict[str, float], path: Path = MODEL_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "feature_names": FEATURE_NAMES,
            "metrics": metrics,
        },
        path,
    )
    return path


def load_model(path: Path = MODEL_PATH) -> ModelArtifact:
    payload = joblib.load(path)
    return ModelArtifact(
        model=payload["model"],
        feature_names=list(payload["feature_names"]),
        metrics=dict(payload.get("metrics", {})),
    )


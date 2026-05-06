from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db.models import Prediction
from app.db.seed import seed_database
from app.ml.features import build_training_rows, feature_matrix, labels
from app.ml.model_registry import load_model
from app.ml.predict import predict_video_risk
from app.ml.model_registry import save_model
from sklearn.ensemble import RandomForestClassifier


def _train_test_model(session: Session, model_path: Path) -> None:
    rows = build_training_rows(session)
    model = RandomForestClassifier(
        n_estimators=80,
        random_state=42,
        class_weight="balanced",
        max_depth=5,
    )
    model.fit(feature_matrix(rows), labels(rows))
    save_model(model, {"training_rows": float(len(rows))}, model_path)


def test_video_risk_model_can_be_trained_and_loaded(tmp_path: Path) -> None:
    engine = create_engine("sqlite:///:memory:")
    seed_database(engine, Path("data"))
    model_path = tmp_path / "video_risk_model.joblib"

    with Session(engine) as session:
        _train_test_model(session, model_path)

    artifact = load_model(model_path)

    assert artifact.feature_names
    assert artifact.metrics["training_rows"] == 10.0


def test_predict_video_risk_persists_prediction(tmp_path: Path) -> None:
    engine = create_engine("sqlite:///:memory:")
    seed_database(engine, Path("data"))
    model_path = tmp_path / "video_risk_model.joblib"

    with Session(engine) as session:
        _train_test_model(session, model_path)
        prediction = predict_video_risk(session, "video_104", model_path=model_path)

        stored = session.scalars(select(Prediction)).all()

    assert prediction.video_id == "video_104"
    assert prediction.risk_level in {"medium", "high"}
    assert prediction.risk_score >= 0.4
    assert len(prediction.top_factors) >= 1
    assert len(stored) == 1
    assert stored[0].video_id == "video_104"

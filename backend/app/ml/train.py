from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from app.db.seed import DATA_DIR, seed_database
from app.db.session import engine
from app.ml.features import build_training_rows, feature_matrix, labels
from app.ml.model_registry import MODEL_PATH, save_model
from sqlalchemy.orm import Session


def train_video_risk_model(model_path: Path = MODEL_PATH, reset_seed_data: bool = False) -> dict[str, float]:
    if reset_seed_data:
        seed_database(engine, DATA_DIR)

    with Session(engine) as session:
        rows = build_training_rows(session)

    x = feature_matrix(rows)
    y = labels(rows)
    if len(set(y)) < 2:
        raise ValueError("Training data must contain both underperforming and healthy videos")

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=120,
        random_state=42,
        class_weight="balanced",
        max_depth=5,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)) if len(set(y_test)) > 1 else 0.0,
        "training_rows": float(len(rows)),
    }
    save_model(model, metrics, model_path)
    return metrics


def main() -> None:
    metrics = train_video_risk_model(reset_seed_data=False)
    print(metrics)


if __name__ == "__main__":
    main()


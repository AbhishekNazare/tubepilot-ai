from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestClassifier

from app.agents.creator_agent import CreatorAgent
from app.db.models import AgentRun, AgentStep, Prediction
from app.db.seed import seed_database
from app.ml.features import build_training_rows, feature_matrix, labels
from app.ml.model_registry import MODEL_PATH, save_model


def _train_repo_model(session: Session) -> None:
    rows = build_training_rows(session)
    model = RandomForestClassifier(
        n_estimators=80,
        random_state=42,
        class_weight="balanced",
        max_depth=5,
    )
    model.fit(feature_matrix(rows), labels(rows))
    save_model(model, {"training_rows": float(len(rows))}, MODEL_PATH)


def test_creator_agent_runs_underperformance_workflow() -> None:
    engine = create_engine("sqlite:///:memory:")
    seed_database(engine, Path("data"))

    with Session(engine) as session:
        _train_repo_model(session)
        response = CreatorAgent().run(
            session,
            channel_id="channel_001",
            query="Why did my latest video underperform?",
        )

        run_count = session.scalar(select(func.count(AgentRun.run_id)))
        step_count = session.scalar(select(func.count(AgentStep.step_id)))
        prediction_count = session.scalar(select(func.count(Prediction.prediction_id)))

    assert response.video_id == "video_105"
    assert response.run_id.startswith("run_")
    assert response.answer
    assert response.citations
    assert [step.tool for step in response.agent_steps] == [
        "get_recent_videos",
        "get_video_metrics",
        "get_channel_metrics",
        "predict_video_risk",
        "search_creator_docs",
        "generate_action_plan",
    ]
    assert run_count == 1
    assert step_count == 6
    assert prediction_count == 1


import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestClassifier

from app.agents.creator_agent import CreatorAgent
from app.db.seed import DATA_DIR, seed_database
from app.ml.features import build_training_rows, feature_matrix, labels
from app.ml.model_registry import MODEL_PATH, save_model

EVAL_PATH = Path(__file__).with_name("test_questions.json")


def _train_model(session: Session) -> None:
    rows = build_training_rows(session)
    model = RandomForestClassifier(n_estimators=80, random_state=42, class_weight="balanced", max_depth=5)
    model.fit(feature_matrix(rows), labels(rows))
    save_model(model, {"training_rows": float(len(rows))}, MODEL_PATH)


def run() -> dict[str, object]:
    cases = [case for case in json.loads(EVAL_PATH.read_text()) if case["type"] == "agent"]
    engine = create_engine("sqlite:///:memory:")
    seed_database(engine, DATA_DIR)

    results = []
    with Session(engine) as session:
        _train_model(session)
        for case in cases:
            response = CreatorAgent().run(session, case["channel_id"], case["query"])
            tools = [step.tool for step in response.agent_steps]
            passed = all(tool in tools for tool in case["expected_tools"]) and bool(response.citations)
            results.append({"id": case["id"], "passed": passed, "tools": tools, "run_id": response.run_id})

    return {"passed": all(item["passed"] for item in results), "results": results}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

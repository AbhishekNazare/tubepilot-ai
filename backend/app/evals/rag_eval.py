import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.seed import reset_database
from app.rag.ingestion import ingest_default_documents
from app.rag.retrieval import search_creator_docs

EVAL_PATH = Path(__file__).with_name("test_questions.json")


def run() -> dict[str, object]:
    cases = [case for case in json.loads(EVAL_PATH.read_text()) if case["type"] == "rag"]
    engine = create_engine("sqlite:///:memory:")
    reset_database(engine)

    results = []
    with Session(engine) as session:
        ingest_default_documents(session)
        for case in cases:
            chunks = search_creator_docs(session, case["query"], top_k=3)
            combined = " ".join(chunk.title + " " + chunk.text for chunk in chunks).lower()
            passed = all(term.lower() in combined for term in case["expected_terms"])
            results.append({"id": case["id"], "passed": passed, "chunks": [chunk.chunk_id for chunk in chunks]})

    return {"passed": all(item["passed"] for item in results), "results": results}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))


from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.agents.tools import (
    generate_action_plan,
    get_channel_metrics,
    get_recent_videos,
    get_video_metrics,
    search_creator_guidance,
)
from app.db.seed import seed_database
from app.rag.ingestion import ingest_default_documents


def test_agent_tools_read_metrics_and_guidance() -> None:
    engine = create_engine("sqlite:///:memory:")
    seed_database(engine, Path("data"))

    with Session(engine) as session:
        ingest_default_documents(session)
        recent_videos = get_recent_videos(session, "channel_001", limit=3)
        latest_metrics = get_video_metrics(session, recent_videos[0].video_id)
        channel_metrics = get_channel_metrics(session, "channel_001")
        chunks = search_creator_guidance(session, "low CTR retention title thumbnail", top_k=2)
        action_plan = generate_action_plan(
            latest_metrics,
            channel_metrics,
            prediction=type(
                "PredictionStub",
                (),
                {
                    "risk_level": "high",
                    "risk_score": 0.81,
                    "top_factors": ["low_ctr", "low_retention"],
                },
            )(),
            citations=chunks,
        )

    assert [video.video_id for video in recent_videos[:2]] == ["video_105", "video_104"]
    assert latest_metrics.video_id == "video_105"
    assert channel_metrics.avg_ctr > 0
    assert len(chunks) == 2
    assert "title-thumbnail" in action_plan


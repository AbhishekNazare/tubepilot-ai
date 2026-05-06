from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.db.models import Channel, ChannelMetricDaily, Video, VideoMetricDaily
from app.db.seed import seed_database


def test_seed_database_loads_synthetic_analytics() -> None:
    engine = create_engine("sqlite:///:memory:")

    counts = seed_database(engine, Path("data"))

    assert counts == {
        "channels": 2,
        "videos": 10,
        "video_metrics_daily": 27,
        "channel_metrics_daily": 10,
    }

    with Session(engine) as session:
        video_count = session.scalar(select(func.count(Video.video_id)))
        metric_count = session.scalar(select(func.count(VideoMetricDaily.metric_id)))
        channel_count = session.scalar(select(func.count(Channel.channel_id)))
        channel_metric_count = session.scalar(select(func.count(ChannelMetricDaily.metric_id)))

        assert video_count == 10
        assert metric_count == 27
        assert channel_count == 2
        assert channel_metric_count == 10


def test_seed_data_contains_risk_signal_variation() -> None:
    engine = create_engine("sqlite:///:memory:")
    seed_database(engine, Path("data"))

    with Session(engine) as session:
        low_ctr_count = session.scalar(
            select(func.count(VideoMetricDaily.metric_id)).where(VideoMetricDaily.ctr < 5.0)
        )
        strong_retention_count = session.scalar(
            select(func.count(VideoMetricDaily.metric_id)).where(
                VideoMetricDaily.retention_percentage > 48.0
            )
        )

        assert low_ctr_count >= 5
        assert strong_retention_count >= 5


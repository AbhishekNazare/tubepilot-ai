from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import ChannelMetricDaily, Video, VideoMetricDaily

FEATURE_NAMES = [
    "views",
    "impressions",
    "ctr",
    "avg_view_duration",
    "retention_percentage",
    "likes",
    "comments",
    "subscriber_delta",
    "channel_avg_ctr",
    "channel_avg_retention",
    "channel_avg_views",
    "view_ratio",
    "ctr_delta",
    "retention_delta",
]


@dataclass(frozen=True)
class VideoFeatureRow:
    video_id: str
    channel_id: str
    title: str
    features: dict[str, float]
    label: int


def _latest_video_metric(session: Session, video_id: str) -> VideoMetricDaily | None:
    return session.scalars(
        select(VideoMetricDaily)
        .where(VideoMetricDaily.video_id == video_id)
        .order_by(VideoMetricDaily.metric_date.desc())
        .limit(1)
    ).first()


def _latest_channel_metric(session: Session, channel_id: str) -> ChannelMetricDaily | None:
    return session.scalars(
        select(ChannelMetricDaily)
        .where(ChannelMetricDaily.channel_id == channel_id)
        .order_by(ChannelMetricDaily.metric_date.desc())
        .limit(1)
    ).first()


def _channel_avg_views(session: Session, channel_id: str) -> float:
    value = session.scalar(
        select(func.avg(VideoMetricDaily.views))
        .join(Video, Video.video_id == VideoMetricDaily.video_id)
        .where(Video.channel_id == channel_id)
    )
    return float(value or 0.0)


def build_video_feature_row(session: Session, video_id: str) -> VideoFeatureRow:
    video = session.get(Video, video_id)
    if video is None:
        raise ValueError(f"Unknown video_id: {video_id}")

    metric = _latest_video_metric(session, video_id)
    if metric is None:
        raise ValueError(f"No metrics found for video_id: {video_id}")

    channel_metric = _latest_channel_metric(session, video.channel_id)
    channel_avg_views = _channel_avg_views(session, video.channel_id)
    channel_avg_ctr = float(channel_metric.avg_ctr if channel_metric else metric.ctr)
    channel_avg_retention = float(
        channel_metric.avg_retention if channel_metric else metric.retention_percentage
    )
    view_ratio = float(metric.views / channel_avg_views) if channel_avg_views else 1.0

    features = {
        "views": float(metric.views),
        "impressions": float(metric.impressions),
        "ctr": float(metric.ctr),
        "avg_view_duration": float(metric.avg_view_duration),
        "retention_percentage": float(metric.retention_percentage),
        "likes": float(metric.likes),
        "comments": float(metric.comments),
        "subscriber_delta": float(metric.subscribers_gained - metric.subscribers_lost),
        "channel_avg_ctr": channel_avg_ctr,
        "channel_avg_retention": channel_avg_retention,
        "channel_avg_views": channel_avg_views,
        "view_ratio": view_ratio,
        "ctr_delta": float(metric.ctr - channel_avg_ctr),
        "retention_delta": float(metric.retention_percentage - channel_avg_retention),
    }

    label = int(
        view_ratio < 0.65
        or features["ctr_delta"] <= -1.5
        or features["retention_delta"] <= -8.0
        or features["subscriber_delta"] < 90
    )

    return VideoFeatureRow(
        video_id=video.video_id,
        channel_id=video.channel_id,
        title=video.title,
        features=features,
        label=label,
    )


def build_training_rows(session: Session) -> list[VideoFeatureRow]:
    video_ids = session.scalars(select(Video.video_id).order_by(Video.published_at)).all()
    return [build_video_feature_row(session, video_id) for video_id in video_ids]


def feature_matrix(rows: list[VideoFeatureRow]) -> list[list[float]]:
    return [[row.features[name] for name in FEATURE_NAMES] for row in rows]


def labels(rows: list[VideoFeatureRow]) -> list[int]:
    return [row.label for row in rows]

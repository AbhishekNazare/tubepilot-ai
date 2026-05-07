from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ChannelMetricDaily, Document, Video, VideoMetricDaily
from app.ml.predict import VideoRiskPrediction, predict_video_risk
from app.rag.ingestion import ingest_default_documents
from app.rag.retrieval import RetrievedChunk, search_creator_docs


@dataclass(frozen=True)
class VideoSnapshot:
    video_id: str
    title: str
    views: int
    impressions: int
    ctr: float
    avg_view_duration: float
    retention_percentage: float
    subscriber_delta: int


@dataclass(frozen=True)
class ChannelSnapshot:
    channel_id: str
    avg_ctr: float
    avg_retention: float
    total_views: int


def get_recent_videos(session: Session, channel_id: str, limit: int = 3) -> list[Video]:
    return list(
        session.scalars(
            select(Video)
            .where(Video.channel_id == channel_id)
            .order_by(Video.published_at.desc())
            .limit(limit)
        )
    )


def get_video_metrics(session: Session, video_id: str) -> VideoSnapshot:
    video = session.get(Video, video_id)
    if video is None:
        raise ValueError(f"Unknown video_id: {video_id}")

    metric = session.scalars(
        select(VideoMetricDaily)
        .where(VideoMetricDaily.video_id == video_id)
        .order_by(VideoMetricDaily.metric_date.desc())
        .limit(1)
    ).first()
    if metric is None:
        raise ValueError(f"No metrics found for video_id: {video_id}")

    return VideoSnapshot(
        video_id=video.video_id,
        title=video.title,
        views=metric.views,
        impressions=metric.impressions,
        ctr=metric.ctr,
        avg_view_duration=metric.avg_view_duration,
        retention_percentage=metric.retention_percentage,
        subscriber_delta=metric.subscribers_gained - metric.subscribers_lost,
    )


def get_channel_metrics(session: Session, channel_id: str) -> ChannelSnapshot:
    metric = session.scalars(
        select(ChannelMetricDaily)
        .where(ChannelMetricDaily.channel_id == channel_id)
        .order_by(ChannelMetricDaily.metric_date.desc())
        .limit(1)
    ).first()
    if metric is None:
        raise ValueError(f"No channel metrics found for channel_id: {channel_id}")

    return ChannelSnapshot(
        channel_id=channel_id,
        avg_ctr=metric.avg_ctr,
        avg_retention=metric.avg_retention,
        total_views=metric.total_views,
    )


def predict_video_underperformance(session: Session, video_id: str) -> VideoRiskPrediction:
    return predict_video_risk(session, video_id, persist=True)


def search_creator_guidance(session: Session, query: str, top_k: int = 3) -> list[RetrievedChunk]:
    if session.scalar(select(Document.document_id).limit(1)) is None:
        ingest_default_documents(session)
    return search_creator_docs(session, query, top_k=top_k)


def generate_action_plan(
    video: VideoSnapshot,
    channel: ChannelSnapshot,
    prediction: VideoRiskPrediction,
    citations: list[RetrievedChunk],
) -> str:
    ctr_gap = video.ctr - channel.avg_ctr
    retention_gap = video.retention_percentage - channel.avg_retention
    citation_titles = ", ".join(dict.fromkeys(chunk.title for chunk in citations))
    factors = ", ".join(prediction.top_factors)

    return (
        f"{video.title} is currently {prediction.risk_level} risk "
        f"({prediction.risk_score:.2f}). The main signals are {factors}. "
        f"CTR is {video.ctr:.1f}% versus the channel baseline of {channel.avg_ctr:.1f}% "
        f"({ctr_gap:+.1f} points), and retention is {video.retention_percentage:.1f}% "
        f"versus {channel.avg_retention:.1f}% ({retention_gap:+.1f} points). "
        "Next, tighten the title-thumbnail promise, make the first 30 seconds prove the payoff, "
        "and compare the topic against recent winners before the next upload. "
        f"Relevant guidance came from: {citation_titles}."
    )

